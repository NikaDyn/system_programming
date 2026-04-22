const API = window.location.origin;

let map, markers = [];
let currentTab = 'list';
let currentFilter = 'all';
let favoriteIds = new Set();
let allPlaces = [];
let categories = [];
let isLoginMode = true;

function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) loader.style.display = 'none';
}

function showLoader() {
    const loader = document.getElementById('loader');
    if (loader) loader.style.display = 'flex';
}

function renderCards(dataArray) {
    const container = document.getElementById('items-grid');
    if (!container) return;

    container.innerHTML = '';

    dataArray.forEach(item => {
        const cardHTML = `
            <div class="place-card" data-category="${item.category}" data-is-popular="${item.is_popular}" data-is-new="${item.is_new}">
                <div class="place-card-header">
                    <span class="place-cat-badge">${item.category}</span>
                    <button class="fav-btn" data-id="${item.id}" title="Додати в обране">☆</button>
                </div>
                <div class="place-name">${item.name}</div>
                <div class="place-desc">${item.description}</div>
                <div class="place-meta">
                    <div class="place-address">
                        <svg width="10" height="12" viewBox="0 0 10 12" fill="none"><path d="M5 0C2.24 0 0 2.24 0 5C0 8.75 5 12 5 12C5 12 10 8.75 10 5C10 2.24 7.76 0 5 0ZM5 6.5C4.17 6.5 3.5 5.83 3.5 5C3.5 4.17 4.17 3.5 5 3.5C5.83 3.5 6.5 4.17 6.5 5C6.5 5.83 5.83 6.5 5 6.5Z" fill="currentColor"/></svg>
                        ${item.address}
                    </div>
                    <div class="place-tags">
                        ${item.is_new ? '<span class="tag tag-new">Нове</span>' : ''}
                        ${item.is_popular ? '<span class="tag tag-popular">Топ</span>' : ''}
                        <span class="tag" style="background:#e8f4fd;color:#2b6cb0">★ ${item.rating}</span>
                    </div>
                </div>
            </div>`;

        container.insertAdjacentHTML('beforeend', cardHTML);
    });

    container.querySelectorAll('.fav-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            btn.classList.toggle('is-active');
            btn.textContent = btn.classList.contains('is-active') ? '★' : '☆';
        });
    });
}

async function loadData() {
    showLoader();

    try {
        const response = await fetch('/static/data.json');

        if (!response.ok) {
            throw new Error(`HTTP помилка: ${response.status}`);
        }

        const data = await response.json();
        renderCards(data);

    } catch (error) {
        const container = document.getElementById('items-grid');
        if (container) {
            container.innerHTML = `
                <div class="error-message">
                    <div class="error-icon">⚠️</div>
                    <h3>Вибачте, дані тимчасово недоступні.</h3>
                    <p>Спробуйте оновити сторінку.</p>
                </div>`;
        }
    } finally {
        hideLoader();
    }
}

function filterLocalCards(filter) {
    const cards = document.querySelectorAll('#items-grid .place-card');

    cards.forEach(card => {
        let visible = false;

        if (filter === 'all') {
            visible = true;
        } else if (filter === 'popular') {
            visible = card.dataset.isPopular === 'true';
        } else if (filter === 'new') {
            visible = card.dataset.isNew === 'true';
        } else {
            visible = card.dataset.category === filter;
        }

        card.classList.toggle('hidden', !visible);
    });
}

function initMap() {
    map = L.map('map', { zoomControl: false }).setView([48.9226, 24.7111], 14);
    L.control.zoom({ position: 'bottomright' }).addTo(map);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap contributors, © CARTO'
    }).addTo(map);

    map.on('click', (e) => {
        const latEl = document.getElementById('form-lat');
        const lngEl = document.getElementById('form-lng');
        if (latEl && lngEl) {
            latEl.value = e.latlng.lat.toFixed(6);
            lngEl.value = e.latlng.lng.toFixed(6);
            switchTab('add');
            showToast('📍 Координати вибрано', 'info');
        }
    });

    setTimeout(() => {
        const hint = document.getElementById('map-hint');
        if (hint) hint.style.opacity = '0';
    }, 4000);
}

function clearMarkers() {
    markers.forEach(m => map.removeLayer(m));
    markers = [];
}

function renderMarkers(places) {
    clearMarkers();
    places.forEach(p => {
        const icon = L.divIcon({
            className: '',
            html: `<svg width="28" height="36" viewBox="0 0 28 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14 0C6.27 0 0 6.27 0 14C0 24.5 14 36 14 36C14 36 28 24.5 28 14C28 6.27 21.73 0 14 0Z" fill="#e84c2b"/>
                <circle cx="14" cy="14" r="6" fill="white"/>
            </svg>`,
            iconSize: [28, 36],
            iconAnchor: [14, 36],
            popupAnchor: [0, -36]
        });

        const marker = L.marker([p.latitude, p.longitude], { icon }).addTo(map);
        marker.bindPopup(`
            <div style="font-family:'DM Sans',sans-serif; min-width:160px">
                <div style="font-weight:700;font-size:14px;margin-bottom:4px">${p.name}</div>
                <div style="font-size:11px;color:#9b9080">${p.address || 'Івано-Франківськ'}</div>
                ${p.description ? `<div style="font-size:12px;margin-top:6px;color:#555">${p.description}</div>` : ''}
                ${p.is_popular ? '<span style="background:#fee2e2;color:#dc2626;font-size:10px;font-weight:700;padding:2px 8px;border-radius:100px;margin-top:6px;display:inline-block">🔥 Популярне</span>' : ''}
            </div>
        `);

        marker.on('click', () => highlightCard(p.id));
        marker._placeId = p.id;
        markers.push(marker);
    });
}

function panToPlace(lat, lng, id) {
    map.flyTo([lat, lng], 16, { duration: 0.8 });
    markers.forEach(m => {
        if (m._placeId === id) m.openPopup();
    });
}

function highlightCard(id) {
    document.querySelectorAll('.place-card').forEach(c => c.classList.remove('selected'));
    const card = document.getElementById(`card-${id}`);
    if (card) {
        card.classList.add('selected');
        card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

async function fetchCategories() {
    try {
        const res = await fetch(`${API}/categories/`);
        categories = await res.json();
        renderCategoryChips();
        renderCategorySelect();
    } catch (e) {}
}

function renderCategoryChips() {
    const wrap = document.getElementById('cat-chips');
    if (!wrap) return;
    wrap.innerHTML = categories.slice(0, 4).map(c =>
        `<button class="filter-chip" data-filter="cat-${c.id}">${c.name}</button>`
    ).join('');

    wrap.querySelectorAll('.filter-chip').forEach(btn => {
        btn.addEventListener('click', () => {
            const catId = parseInt(btn.dataset.filter.replace('cat-', ''));
            applyFilter('cat', catId, btn);
        });
    });
}

function renderCategorySelect() {
    const sel = document.getElementById('form-category');
    if (!sel) return;
    sel.innerHTML = `<option value="" disabled selected>Виберіть категорію</option>` +
        categories.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
}

async function fetchPlaces(params = {}) {
    try {
        const url = new URL(`${API}/places/`);
        Object.keys(params).forEach(k => url.searchParams.set(k, params[k]));
        const res = await fetch(url);
        const places = await res.json();
        allPlaces = places;

        if (getToken()) await syncFavorites();

        renderMarkers(allPlaces);
        if (currentTab === 'list') renderList(allPlaces);
    } catch (e) { console.error(e); }
}

async function syncFavorites() {
    try {
        const res = await fetch(`${API}/favorites/`, { headers: authHeaders() });
        if (res.ok) {
            const favs = await res.json();
            favoriteIds = new Set(favs.map(f => f.place_id));
        }
    } catch (e) {}
}

async function fetchFavorites() {
    if (!getToken()) { renderFavEmptyLogin(); return; }
    try {
        const res = await fetch(`${API}/favorites/`, { headers: authHeaders() });
        const favs = await res.json();
        const places = favs.map(f => f.place).filter(Boolean);
        renderList(places, true);
    } catch (e) {}
}

function renderList(places, isFav = false) {
    const content = document.getElementById('sidebar-content');
    if (!content) return;

    if (places.length === 0) {
        content.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">${isFav ? '⭐' : '🗺'}</div>
                <h3>${isFav ? 'Обране порожнє' : 'Нічого не знайдено'}</h3>
                <p>${isFav ? 'Додайте місця, натиснувши зірочку' : 'Спробуйте змінити фільтр'}</p>
            </div>`;
        return;
    }

    const listEl = document.createElement('div');
    listEl.className = 'places-list';

    places.forEach(p => {
        const isFavPlace = favoriteIds.has(p.id);
        const catName = categories.find(c => c.id === p.category_id)?.name || '';

        const card = document.createElement('div');
        card.className = 'place-card';
        card.id = `card-${p.id}`;
        card.dataset.category = p.category_id || '';
        card.dataset.isNew = p.is_new ? 'true' : 'false';
        card.dataset.isPopular = p.is_popular ? 'true' : 'false';

        card.innerHTML = `
            <button class="delete-btn">видалити</button>
            <div class="place-card-header">
                <span class="place-cat-badge">${catName}</span>
                <button class="fav-btn ${isFavPlace ? 'is-active' : ''}" title="${isFavPlace ? 'Прибрати з обраного' : 'Додати в обране'}">
                    ${isFavPlace ? '★' : '☆'}
                </button>
            </div>
            <div class="place-name">${p.name}</div>
            <div class="place-desc">${p.description || 'Опис відсутній'}</div>
            <div class="place-meta">
                <div class="place-address">
                    <svg width="10" height="12" viewBox="0 0 10 12" fill="none"><path d="M5 0C2.24 0 0 2.24 0 5C0 8.75 5 12 5 12C5 12 10 8.75 10 5C10 2.24 7.76 0 5 0ZM5 6.5C4.17 6.5 3.5 5.83 3.5 5C3.5 4.17 4.17 3.5 5 3.5C5.83 3.5 6.5 4.17 6.5 5C6.5 5.83 5.83 6.5 5 6.5Z" fill="currentColor"/></svg>
                    ${p.address || 'Івано-Франківськ'}
                </div>
                <div class="place-tags">
                    ${p.is_new ? '<span class="tag tag-new">Нове</span>' : ''}
                    ${p.is_popular ? '<span class="tag tag-popular">Топ</span>' : ''}
                </div>
            </div>`;

        card.addEventListener('click', () => panToPlace(p.latitude, p.longitude, p.id));

        card.querySelector('.fav-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            toggleFav(p.id, card.querySelector('.fav-btn').classList.contains('is-active'), card.querySelector('.fav-btn'));
        });

        card.querySelector('.delete-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            deletePlace(p.id);
        });

        listEl.appendChild(card);
    });

    content.innerHTML = '';
    content.appendChild(listEl);
}

function renderFavEmptyLogin() {
    const content = document.getElementById('sidebar-content');
    content.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">🔐</div>
            <h3>Потрібна авторизація</h3>
            <p>Увійдіть, щоб бачити збережені місця</p>
            <br>
            <button class="btn btn-accent cta-btn" style="margin:0 auto; display:block; padding:10px 24px; font-size:13px;" id="fav-login-btn">Увійти</button>
        </div>`;
    document.getElementById('fav-login-btn')?.addEventListener('click', () => openModal(true));
}

function renderAddForm() {
    const content = document.getElementById('sidebar-content');
    content.innerHTML = `
        <div class="add-form-wrap" id="add-section">
            <h2 class="form-section-title">Нова локація</h2>
            <p class="form-section-sub">Натисніть на карті, щоб заповнити координати</p>
            <form id="add-place-form">
                <div class="field">
                    <label>Назва</label>
                    <input type="text" id="form-name" placeholder="Наприклад: Ратуша" required>
                </div>
                <div class="field">
                    <label>Адреса</label>
                    <input type="text" id="form-address" placeholder="вул. Грушевського, 1">
                </div>
                <div class="field-row">
                    <div class="field">
                        <label>Широта</label>
                        <input type="number" step="any" id="form-lat" placeholder="48.9226" required>
                    </div>
                    <div class="field">
                        <label>Довгота</label>
                        <input type="number" step="any" id="form-lng" placeholder="24.7111" required>
                    </div>
                </div>
                <div class="field">
                    <label>Категорія</label>
                    <select id="form-category" required></select>
                </div>
                <div class="field">
                    <label>Опис</label>
                    <textarea id="form-desc" rows="3" placeholder="Розкажіть про це місце..."></textarea>
                </div>
                <button type="submit" class="cta-btn form-submit">Опублікувати ↗</button>
            </form>
            <div class="map-hint-form">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>
                Тільки адміністратори можуть додавати локації
            </div>
        </div>`;

    renderCategorySelect();
    document.getElementById('add-place-form').addEventListener('submit', submitPlace);
}

function applyFilter(type, catId = null, clickedBtn = null) {
    currentFilter = type;

    document.querySelectorAll('.filter-chip').forEach(c => {
        c.classList.remove('active', 'active-blue');
    });

    if (type === 'all') {
        document.querySelector('[data-filter="all"]')?.classList.add('active');
        fetchPlaces();
        filterLocalCards('all');
    } else if (type === 'popular') {
        document.querySelector('[data-filter="popular"]')?.classList.add('active');
        fetchPlaces({ is_popular: true });
        filterLocalCards('popular');
    } else if (type === 'new') {
        document.querySelector('[data-filter="new"]')?.classList.add('active');
        fetchPlaces({ is_new: true });
        filterLocalCards('new');
    } else if (type === 'cat' && catId) {
        if (clickedBtn) clickedBtn.classList.add('active-blue');
        fetchPlaces({ category_id: catId });
    }
}

async function toggleFav(id, isFav, btnEl) {
    if (!getToken()) { openModal(true); return; }

    const method = isFav ? 'DELETE' : 'POST';
    const res = await fetch(`${API}/favorites/${id}`, { method, headers: authHeaders() });

    if (res.ok) {
        btnEl.classList.toggle('is-active');
        const nowActive = btnEl.classList.contains('is-active');
        btnEl.textContent = nowActive ? '★' : '☆';
        if (nowActive) { favoriteIds.add(id); showToast('Додано в обране ✨'); }
        else { favoriteIds.delete(id); showToast('Видалено з обраного', 'info'); }
        if (currentTab === 'fav') fetchFavorites();
    } else if (res.status === 401) { openModal(true); }
}

async function deletePlace(id) {
    if (!confirm('Видалити цю локацію?')) return;
    const res = await fetch(`${API}/places/${id}`, { method: 'DELETE', headers: authHeaders() });
    if (res.ok) {
        showToast('Локацію видалено');
        await fetchPlaces();
        if (currentTab === 'list') renderList(allPlaces);
    } else if (res.status === 401) { openModal(true); }
    else if (res.status === 403) showToast('Тільки адмін може видаляти', 'error');
}

async function submitPlace(e) {
    e.preventDefault();
    const submitBtn = e.target.querySelector('.cta-btn');
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span class="spinner-inline"></span> Обробка...`;

    const data = {
        name: document.getElementById('form-name').value,
        description: document.getElementById('form-desc').value,
        address: document.getElementById('form-address').value,
        latitude: parseFloat(document.getElementById('form-lat').value),
        longitude: parseFloat(document.getElementById('form-lng').value),
        category_id: parseInt(document.getElementById('form-category').value),
        is_new: true,
        is_popular: false
    };

    try {
        const res = await fetch(`${API}/places/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', ...authHeaders() },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            showToast('Локацію опубліковано! 🎉');
            e.target.reset();
            switchTab('list');
            await fetchPlaces();
        } else if (res.status === 401) { openModal(true); }
        else if (res.status === 403) showToast('Тільки адмін може додавати місця', 'error');
        else showToast('Помилка при збереженні', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Опублікувати ↗';
    }
}

function switchTab(tab) {
    currentTab = tab;
    document.querySelectorAll('.sidebar-tab').forEach(t => t.classList.remove('active'));
    document.getElementById(`tab-${tab}`)?.classList.add('active');

    if (tab === 'list') renderList(allPlaces);
    else if (tab === 'fav') fetchFavorites();
    else if (tab === 'add') renderAddForm();
}

function getToken() { return localStorage.getItem('if_token'); }

function authHeaders() {
    const t = getToken();
    return t ? { 'Authorization': `Bearer ${t}` } : {};
}

function openModal(login) {
    isLoginMode = login;
    updateModalUI();
    document.getElementById('auth-modal').classList.add('open');
}

function closeModal() {
    document.getElementById('auth-modal').classList.remove('open');
}

function updateModalUI() {
    document.getElementById('modal-title').textContent = isLoginMode ? 'З поверненням' : 'Реєстрація';
    document.getElementById('modal-sub').textContent = isLoginMode ? 'Увійдіть у свій акаунт' : 'Створіть новий акаунт';
    document.getElementById('modal-btn').textContent = isLoginMode ? 'Увійти' : 'Зареєструватися';
    document.getElementById('toggle-text').textContent = isLoginMode ? 'Немає акаунту?' : 'Вже є акаунт?';
    document.getElementById('toggle-link-btn').textContent = isLoginMode ? ' Зареєструватися' : ' Увійти';
}

function logout() {
    localStorage.removeItem('if_token');
    localStorage.removeItem('if_user');
    favoriteIds.clear();
    updateHeaderAuth();
    renderList(allPlaces);
    showToast('Ви вийшли');
}

function updateHeaderAuth() {
    const user = localStorage.getItem('if_user');
    const el = document.getElementById('header-auth');
    if (!el) return;

    if (user) {
        el.innerHTML = `
            <span style="color:rgba(255,255,255,0.5);font-size:13px">${user}</span>
            <button class="btn btn-ghost" id="logout-btn">Вийти</button>`;
        document.getElementById('logout-btn')?.addEventListener('click', logout);
    } else {
        el.innerHTML = `
            <button class="btn btn-ghost" id="header-login-btn">Вхід</button>
            <button class="btn btn-accent" id="header-register-btn">Реєстрація</button>`;
        document.getElementById('header-login-btn')?.addEventListener('click', () => openModal(true));
        document.getElementById('header-register-btn')?.addEventListener('click', () => openModal(false));
    }
}

function showToast(msg, type = 'success') {
    const container = document.getElementById('toast-container');
    const el = document.createElement('div');
    el.className = `toast toast-${type}`;
    el.textContent = msg;
    container.appendChild(el);
    setTimeout(() => {
        el.style.transition = 'opacity 0.3s';
        el.style.opacity = '0';
        setTimeout(() => el.remove(), 300);
    }, 2800);
}

window.addEventListener('load', async () => {
    initMap();
    updateHeaderAuth();

    const burgerBtn = document.getElementById('burger-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileClose = document.getElementById('mobile-menu-close');

    burgerBtn.addEventListener('click', () => {
        burgerBtn.classList.toggle('is-open');
        mobileMenu.classList.toggle('is-open');
        document.body.classList.toggle('no-scroll');
    });

    mobileClose.addEventListener('click', () => {
        burgerBtn.classList.remove('is-open');
        mobileMenu.classList.remove('is-open');
        document.body.classList.remove('no-scroll');
    });

    document.querySelectorAll('.mobile-nav-link').forEach(link => {
        link.addEventListener('click', () => {
            burgerBtn.classList.remove('is-open');
            mobileMenu.classList.remove('is-open');
            document.body.classList.remove('no-scroll');
        });
    });

    document.getElementById('mobile-login-btn')?.addEventListener('click', () => {
        burgerBtn.classList.remove('is-open');
        mobileMenu.classList.remove('is-open');
        document.body.classList.remove('no-scroll');
        openModal(true);
    });

    document.getElementById('modal-close-btn').addEventListener('click', closeModal);
    document.getElementById('auth-modal').addEventListener('click', (e) => {
        if (e.target === document.getElementById('auth-modal')) closeModal();
    });
    document.getElementById('toggle-link-btn').addEventListener('click', () => {
        isLoginMode = !isLoginMode;
        updateModalUI();
    });

    document.getElementById('auth-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('auth-email').value;
        const password = document.getElementById('auth-password').value;
        const btn = document.getElementById('modal-btn');

        btn.disabled = true;
        btn.innerHTML = `<span class="spinner-inline"></span> Обробка...`;

        try {
            let res;
            if (isLoginMode) {
                const body = new FormData();
                body.append('username', email);
                body.append('password', password);
                res = await fetch(`${API}/users/login`, { method: 'POST', body });
            } else {
                res = await fetch(`${API}/users/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password, full_name: email.split('@')[0] })
                });
            }

            if (res.ok) {
                const data = await res.json();
                if (isLoginMode) {
                    localStorage.setItem('if_token', data.access_token);
                    localStorage.setItem('if_user', email.split('@')[0]);
                    closeModal();
                    updateHeaderAuth();
                    await syncFavorites();
                    renderList(allPlaces);
                    showToast('Успішний вхід! 👋');
                } else {
                    isLoginMode = true;
                    updateModalUI();
                    showToast('Реєстрація успішна! Увійдіть');
                }
            } else {
                showToast('Невірний email або пароль', 'error');
            }
        } catch {
            showToast('Сервер не відповідає', 'error');
        } finally {
            btn.disabled = false;
            btn.textContent = isLoginMode ? 'Увійти' : 'Зареєструватися';
        }
    });

    document.querySelectorAll('.filter-chip[data-filter]').forEach(btn => {
        btn.addEventListener('click', () => {
            const f = btn.dataset.filter;
            if (f === 'all') applyFilter('all');
            else if (f === 'popular') applyFilter('popular');
            else if (f === 'new') applyFilter('new');
        });
    });

    document.getElementById('tab-list').addEventListener('click', () => switchTab('list'));
    document.getElementById('tab-fav').addEventListener('click', () => switchTab('fav'));
    document.getElementById('tab-add').addEventListener('click', () => switchTab('add'));

    await loadData();
    await fetchCategories();
    await fetchPlaces();
    renderList(allPlaces);
});