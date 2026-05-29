/**
 * RW EduPlatform – Frontend API Client
 * Drop this script into your HTML pages to connect to the Django backend.
 * Usage: <script src="api.js"></script>
 */

const API_BASE = window.location.hostname === 'localhost'
  ? 'http://localhost:8000/api/v1'
  : '/api/v1';

const WS_BASE = window.location.hostname === 'localhost'
  ? 'ws://localhost:8001/ws'
  : `wss://${window.location.host}/ws`;

/* ── TOKEN HELPERS ──────────────────────────────────────────────────────── */
const Auth = {
  getAccess()  { return localStorage.getItem('rw_access'); },
  getRefresh() { return localStorage.getItem('rw_refresh'); },
  setTokens(access, refresh) {
    localStorage.setItem('rw_access',  access);
    localStorage.setItem('rw_refresh', refresh);
  },
  clear() {
    localStorage.removeItem('rw_access');
    localStorage.removeItem('rw_refresh');
    localStorage.removeItem('rw_user');
  },
  getUser() {
    try { return JSON.parse(localStorage.getItem('rw_user') || 'null'); }
    catch { return null; }
  },
  setUser(user) { localStorage.setItem('rw_user', JSON.stringify(user)); },
  isLoggedIn()  { return !!this.getAccess(); },
};

/* ── HTTP CLIENT ────────────────────────────────────────────────────────── */
async function apiFetch(endpoint, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  if (Auth.isLoggedIn()) {
    headers['Authorization'] = `Bearer ${Auth.getAccess()}`;
  }

  let response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  // Auto-refresh token on 401
  if (response.status === 401 && Auth.getRefresh()) {
    const refreshed = await fetch(`${API_BASE}/auth/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: Auth.getRefresh() }),
    });

    if (refreshed.ok) {
      const data = await refreshed.json();
      Auth.setTokens(data.access, data.refresh || Auth.getRefresh());
      headers['Authorization'] = `Bearer ${data.access}`;
      response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers,
        body: options.body ? JSON.stringify(options.body) : undefined,
      });
    } else {
      Auth.clear();
      window.dispatchEvent(new Event('rw:logout'));
      throw new Error('Session expired. Please log in again.');
    }
  }

  const contentType = response.headers.get('content-type') || '';
  const data = contentType.includes('application/json') ? await response.json() : await response.text();

  if (!response.ok) {
    const message = typeof data === 'object'
      ? (data.detail || data.non_field_errors?.[0] || JSON.stringify(data))
      : data;
    throw new Error(message);
  }

  return data;
}

/* ── AUTH API ───────────────────────────────────────────────────────────── */
const AuthAPI = {
  async login(username, password) {
    const data = await apiFetch('/auth/login/', {
      method: 'POST',
      body: { username, password },
    });
    Auth.setTokens(data.access, data.refresh);
    Auth.setUser(data.user);
    window.dispatchEvent(new CustomEvent('rw:login', { detail: data.user }));
    return data;
  },

  async register(payload) {
    const data = await apiFetch('/auth/register/', {
      method: 'POST',
      body: payload,
    });
    Auth.setTokens(data.access, data.refresh);
    Auth.setUser(data.user);
    return data;
  },

  async logout() {
    try {
      await apiFetch('/auth/logout/', {
        method: 'POST',
        body: { refresh: Auth.getRefresh() },
      });
    } catch (_) { /* ignore */ }
    Auth.clear();
    window.dispatchEvent(new Event('rw:logout'));
  },

  async me() {
    return apiFetch('/auth/me/');
  },

  async changePassword(oldPassword, newPassword) {
    return apiFetch('/auth/change-password/', {
      method: 'POST',
      body: { old_password: oldPassword, new_password: newPassword },
    });
  },
};

/* ── DEMO REQUEST API ───────────────────────────────────────────────────── */
const DemoAPI = {
  async submit(email, name = '', phone = '', message = '') {
    return apiFetch('/auth/demo-request/', {
      method: 'POST',
      body: { email, name, phone, message },
    });
  },
};

/* ── DASHBOARD API ──────────────────────────────────────────────────────── */
const DashboardAPI = {
  async getStats()          { return apiFetch('/dashboard/'); },
  async getRecentActivity() { return apiFetch('/recent-activity/'); },
};

/* ── COURSES API ────────────────────────────────────────────────────────── */
const CoursesAPI = {
  async list(params = {})       { return apiFetch('/courses/?' + new URLSearchParams(params)); },
  async get(id)                  { return apiFetch(`/courses/${id}/`); },
  async create(data)             { return apiFetch('/courses/', { method: 'POST', body: data }); },
  async update(id, data)         { return apiFetch(`/courses/${id}/`, { method: 'PATCH', body: data }); },
  async delete(id)               { return apiFetch(`/courses/${id}/`, { method: 'DELETE' }); },
  async enroll(id)               { return apiFetch(`/courses/${id}/enroll/`, { method: 'POST' }); },
  async unenroll(id)             { return apiFetch(`/courses/${id}/enroll/`, { method: 'DELETE' }); },
  async getTopics(courseId)      { return apiFetch(`/courses/${courseId}/topics/`); },
  async getMaterials(courseId)   { return apiFetch(`/courses/${courseId}/materials/`); },
};

/* ── ATTENDANCE API ─────────────────────────────────────────────────────── */
const AttendanceAPI = {
  async getSessions(params = {})    { return apiFetch('/attendance/sessions/?' + new URLSearchParams(params)); },
  async createSession(data)          { return apiFetch('/attendance/sessions/', { method: 'POST', body: data }); },
  async markBulk(sessionId, records) {
    return apiFetch('/attendance/bulk/', {
      method: 'POST',
      body: { session_id: sessionId, records },
    });
  },
  async getMySummary()               { return apiFetch('/attendance/summary/'); },
  async getStudentSummary(studentId) { return apiFetch(`/attendance/summary/${studentId}/`); },
};

/* ── EXAMS API ──────────────────────────────────────────────────────────── */
const ExamsAPI = {
  async list(params = {}) { return apiFetch('/tests/?' + new URLSearchParams(params)); },
  async get(id)            { return apiFetch(`/tests/${id}/`); },
  async create(data)       { return apiFetch('/tests/', { method: 'POST', body: data }); },
  async start(id)          { return apiFetch(`/tests/${id}/start/`, { method: 'POST' }); },
  async submit(attemptId, answers) {
    return apiFetch('/tests/submit/', {
      method: 'POST',
      body: { attempt_id: attemptId, answers },
    });
  },
  async getResults(params = {}) { return apiFetch('/tests/results/?' + new URLSearchParams(params)); },
};

/* ── FEES API ───────────────────────────────────────────────────────────── */
const FeesAPI = {
  async getPayments(params = {}) { return apiFetch('/fees/payments/?' + new URLSearchParams(params)); },
  async recordPayment(data)       { return apiFetch('/fees/payments/', { method: 'POST', body: data }); },
  async getSummary()              { return apiFetch('/fees/summary/'); },
  async getStructures(params = {}){ return apiFetch('/fees/structures/?' + new URLSearchParams(params)); },
};

/* ── NOTICES API ────────────────────────────────────────────────────────── */
const NoticesAPI = {
  async list(params = {})  { return apiFetch('/notices/?' + new URLSearchParams(params)); },
  async get(id)             { return apiFetch(`/notices/${id}/`); },
  async create(data)        { return apiFetch('/notices/', { method: 'POST', body: data }); },
  async update(id, data)    { return apiFetch(`/notices/${id}/`, { method: 'PATCH', body: data }); },
  async delete(id)          { return apiFetch(`/notices/${id}/`, { method: 'DELETE' }); },
};

/* ── WEBSOCKET (REALTIME NOTIFICATIONS) ─────────────────────────────────── */
class RWSocket {
  constructor() {
    this.ws = null;
    this.reconnectDelay = 2000;
    this.listeners = {};
  }

  connect() {
    if (!Auth.isLoggedIn()) return;
    const token = Auth.getAccess();
    this.ws = new WebSocket(`${WS_BASE}/notifications/?token=${token}`);

    this.ws.onopen = () => {
      console.log('[RW] WebSocket connected');
      this.reconnectDelay = 2000;
      this._emit('open');
    };

    this.ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        this._emit(data.type, data);
        this._emit('message', data);
      } catch (_) {}
    };

    this.ws.onclose = () => {
      console.log('[RW] WebSocket disconnected. Reconnecting...');
      this._emit('close');
      setTimeout(() => this.connect(), this.reconnectDelay);
      this.reconnectDelay = Math.min(this.reconnectDelay * 2, 30000);
    };

    this.ws.onerror = (err) => {
      console.error('[RW] WebSocket error', err);
      this.ws.close();
    };

    // Ping every 30s to keep connection alive
    this._pingInterval = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'ping' }));
      }
    }, 30000);
  }

  on(event, callback) {
    if (!this.listeners[event]) this.listeners[event] = [];
    this.listeners[event].push(callback);
    return this;
  }

  _emit(event, data) {
    (this.listeners[event] || []).forEach(fn => fn(data));
  }

  disconnect() {
    clearInterval(this._pingInterval);
    this.ws?.close();
  }
}

const RWSocketClient = new RWSocket();

/* ── UI HELPERS ─────────────────────────────────────────────────────────── */
const UI = {
  showToast(message, type = 'info') {
    const existing = document.querySelector('.rw-toast-container');
    if (!existing) {
      const container = document.createElement('div');
      container.className = 'rw-toast-container';
      container.style.cssText = `
        position: fixed; top: 80px; right: 20px; z-index: 9999;
        display: flex; flex-direction: column; gap: 10px;
      `;
      document.body.appendChild(container);
    }
    const container = document.querySelector('.rw-toast-container');

    const colors = {
      success: '#00C9A7',
      error:   '#EF4444',
      info:    '#3B82F6',
      warning: '#F5A623',
    };

    const toast = document.createElement('div');
    toast.style.cssText = `
      background: #0B1A3E; color: white;
      border-left: 4px solid ${colors[type] || colors.info};
      padding: 12px 20px; border-radius: 8px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.3);
      font-family: 'DM Sans', sans-serif; font-size: 14px;
      max-width: 340px; animation: slideIn .3s ease;
    `;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
  },

  showLoading(buttonEl) {
    if (!buttonEl) return;
    buttonEl._originalText = buttonEl.textContent;
    buttonEl.disabled = true;
    buttonEl.textContent = 'Loading…';
  },

  hideLoading(buttonEl) {
    if (!buttonEl) return;
    buttonEl.disabled = false;
    buttonEl.textContent = buttonEl._originalText || 'Submit';
  },
};

/* ── DEMO REQUEST FORM (wires up the CTA on the landing page) ───────────── */
document.addEventListener('DOMContentLoaded', () => {
  const ctaSubmit = document.querySelector('.cta-submit');
  const ctaInput  = document.querySelector('.cta-input');

  if (ctaSubmit && ctaInput) {
    ctaSubmit.addEventListener('click', async () => {
      const email = ctaInput.value.trim();
      if (!email || !email.includes('@')) {
        ctaInput.style.borderColor = 'rgba(248,113,113,0.6)';
        setTimeout(() => { ctaInput.style.borderColor = ''; }, 2000);
        return;
      }

      UI.showLoading(ctaSubmit);
      try {
        await DemoAPI.submit(email);
        UI.showToast('Thank you! Our team will contact you within 24 hours.', 'success');
        ctaInput.value = '';
      } catch (err) {
        UI.showToast(err.message || 'Something went wrong. Please try again.', 'error');
      } finally {
        UI.hideLoading(ctaSubmit);
      }
    });
  }
});

/* ── EXPORT (for use as module or global) ───────────────────────────────── */
if (typeof module !== 'undefined') {
  module.exports = { Auth, AuthAPI, DemoAPI, DashboardAPI, CoursesAPI,
                     AttendanceAPI, ExamsAPI, FeesAPI, NoticesAPI,
                     RWSocketClient, UI };
} else {
  window.RW = { Auth, AuthAPI, DemoAPI, DashboardAPI, CoursesAPI,
                AttendanceAPI, ExamsAPI, FeesAPI, NoticesAPI,
                RWSocketClient, UI };
}
