/* ═══════════════════════════════════════════════════════════════
   Smart Transit Predictor — Frontend Logic
   ═══════════════════════════════════════════════════════════════ */

// API base URL (empty = same origin, change for remote backend)
const API_BASE = '';

// Map instance & layers
let map;
let routeLayer;
let markerLayer;

// ──────────────── Initialization ────────────────
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    loadCities();
    setupEventListeners();
    setDefaultDate();
});

// ──────────────── Map Setup ────────────────
function initMap() {
    map = L.map('map', {
        center: [25.0, 93.0],
        zoom: 7,
        zoomControl: true,
        attributionControl: true
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18
    }).addTo(map);

    routeLayer = L.layerGroup().addTo(map);
    markerLayer = L.layerGroup().addTo(map);

    addCityMarkers();
}

function addCityMarkers() {
    const defaultCities = [
        // Mizoram
        { name: 'Aizawl',    lat: 23.7271, lng: 92.7176 },
        // Assam
        { name: 'Silchar',   lat: 24.8333, lng: 92.7789 },
        { name: 'Guwahati',  lat: 26.1445, lng: 91.7362 },
        { name: 'Tezpur',    lat: 26.6338, lng: 92.8006 },
        { name: 'Jorhat',    lat: 26.7509, lng: 94.2037 },
        { name: 'Dibrugarh', lat: 27.4728, lng: 94.9120 },
        // Manipur
        { name: 'Imphal',    lat: 24.8170, lng: 93.9368 },
        // Meghalaya
        { name: 'Shillong',  lat: 25.5788, lng: 91.8933 },
        // Nagaland
        { name: 'Kohima',    lat: 25.6751, lng: 94.1086 },
        { name: 'Dimapur',   lat: 25.9065, lng: 93.7272 },
        // Tripura
        { name: 'Agartala',  lat: 23.8315, lng: 91.2868 },
        // Arunachal Pradesh
        { name: 'Itanagar',  lat: 27.0844, lng: 93.6053 },
        // Sikkim
        { name: 'Gangtok',   lat: 27.3389, lng: 88.6065 },
    ];

    defaultCities.forEach(city => {
        const marker = L.circleMarker([city.lat, city.lng], {
            radius: 6,
            fillColor: '#06b6d4',
            color: '#0e7490',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8
        });
        marker.bindTooltip(city.name, {
            permanent: true,
            direction: 'top',
            offset: [0, -10],
            className: 'city-tooltip'
        });
        markerLayer.addLayer(marker);
    });
}

// ──────────────── Load Cities ────────────────
async function loadCities() {
    const fromSelect = document.getElementById('from-city');
    try {
        const response = await fetch(`${API_BASE}/api/cities`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();

        fromSelect.innerHTML = '<option value="">Select starting city</option>';
        data.cities.forEach(city => {
            const opt = document.createElement('option');
            opt.value = city.name;
            opt.textContent = city.state ? `${city.name}, ${city.state}` : city.name;
            fromSelect.appendChild(opt);
        });
    } catch (error) {
        console.warn('API unavailable, using fallback cities:', error.message);
        const fallback = [
            'Aizawl', 'Silchar', 'Guwahati', 'Tezpur', 'Jorhat',
            'Dibrugarh', 'Imphal', 'Shillong', 'Kohima', 'Dimapur',
            'Agartala', 'Itanagar', 'Gangtok'
        ];
        fromSelect.innerHTML = '<option value="">Select starting city</option>';
        fallback.forEach(name => {
            const opt = document.createElement('option');
            opt.value = name;
            opt.textContent = name;
            fromSelect.appendChild(opt);
        });
    }
}

// ──────────────── Event Listeners ────────────────
function setupEventListeners() {
    const fromSelect = document.getElementById('from-city');
    const checkBtn = document.getElementById('check-btn');

    fromSelect.addEventListener('change', handleFromCityChange);
    checkBtn.addEventListener('click', checkRoute);
}

async function handleFromCityChange(e) {
    const city = e.target.value;
    const toSelect = document.getElementById('to-city');
    toSelect.innerHTML = '<option value="">Select destination</option>';

    if (!city) return;

    try {
        const response = await fetch(`${API_BASE}/api/destinations/${encodeURIComponent(city)}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();

        data.destinations.forEach(dest => {
            const opt = document.createElement('option');
            opt.value = dest;
            opt.textContent = dest;
            toSelect.appendChild(opt);
        });
    } catch (error) {
        console.warn('Failed to load destinations, using fallback:', error.message);
        const allCities = [
            'Aizawl', 'Silchar', 'Guwahati', 'Imphal',
            'Shillong', 'Agartala', 'Dimapur', 'Kohima',
            'Itanagar', 'Tezpur'
        ];
        allCities.filter(c => c !== city).forEach(dest => {
            const opt = document.createElement('option');
            opt.value = dest;
            opt.textContent = dest;
            toSelect.appendChild(opt);
        });
    }
}

// ──────────────── Default Date ────────────────
function setDefaultDate() {
    const dateInput = document.getElementById('travel-date');
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;
    dateInput.min = today;
}

// ──────────────── Check Route ────────────────
async function checkRoute() {
    const fromCity = document.getElementById('from-city').value;
    const toCity = document.getElementById('to-city').value;
    const date = document.getElementById('travel-date').value;

    if (!fromCity || !toCity || !date) {
        showNotification('Please select origin, destination, and travel date.', 'warning');
        return;
    }

    if (fromCity === toCity) {
        showNotification('Origin and destination cannot be the same.', 'warning');
        return;
    }

    const btn = document.getElementById('check-btn');
    const btnText = btn.querySelector('.btn-text');
    const btnLoader = btn.querySelector('.btn-loader');

    // Show loading state
    btn.disabled = true;
    btnText.textContent = 'Analyzing Route…';
    btnLoader.classList.remove('hidden');

    try {
        const response = await fetch(`${API_BASE}/api/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                from_city: fromCity,
                to_city: toCity,
                date: date
            })
        });

        if (!response.ok) {
            let detail = 'Prediction failed';
            try {
                const errBody = await response.json();
                detail = errBody.detail || detail;
            } catch (_) { /* ignore parse error */ }
            throw new Error(detail);
        }

        const data = await response.json();
        displayResults(data);
        drawRouteOnMap(data);

        if (data.route_info) {
            showRouteInfo(data.route_info);
        }

    } catch (error) {
        console.error('Prediction error:', error);
        showNotification(error.message || 'Failed to check route. Please try again.', 'error');
    } finally {
        btn.disabled = false;
        btnText.textContent = 'Check Route Safety';
        btnLoader.classList.add('hidden');
    }
}

// ──────────────── Display Results ────────────────
function displayResults(data) {
    const resultsSection = document.getElementById('results-section');
    resultsSection.classList.remove('hidden');

    // Smooth scroll with slight delay for animation feel
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);

    updateRiskGauge(data.risk_level, data.risk_label);
    updateConfidence(data.confidence);
    updateWeather(data.weather);
    updateReasons(data.reasons);
    updateSegments(data.segments);
}

// ──────────────── Risk Gauge ────────────────
function updateRiskGauge(level, label) {
    const gauge = document.getElementById('risk-gauge');
    const riskLabel = document.getElementById('risk-label');
    const riskIcon = document.getElementById('risk-icon');

    // Remove previous risk classes
    gauge.classList.remove('risk-safe', 'risk-caution', 'risk-danger');

    const classMap = { 0: 'safe', 1: 'caution', 2: 'danger' };
    const iconMap = { 0: '✅', 1: '⚠️', 2: '🚫' };
    const degMap = { 0: 90, 1: 200, 2: 330 };

    const riskClass = classMap[level] || 'safe';

    // Start at 0 then animate to target
    gauge.style.setProperty('--gauge-deg', '0deg');
    gauge.classList.add(`risk-${riskClass}`);

    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            gauge.style.setProperty('--gauge-deg', `${degMap[level] || 0}deg`);
        });
    });

    riskLabel.textContent = (label || riskClass).toUpperCase();
    riskIcon.textContent = iconMap[level] || '—';
}

function updateConfidence(confidence) {
    const el = document.getElementById('confidence');
    if (confidence !== undefined && confidence !== null) {
        el.textContent = typeof confidence === 'number'
            ? `${(confidence * 100).toFixed(1)}%`
            : confidence;
    } else {
        el.textContent = '—';
    }
}

// ──────────────── Weather ────────────────
function updateWeather(weather) {
    if (!weather) return;

    const setVal = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
    };

    setVal('weather-rainfall',
        weather.rainfall_24h != null ? `${Number(weather.rainfall_24h).toFixed(1)} mm` : '—');
    setVal('weather-temperature',
        weather.temperature != null ? `${Number(weather.temperature).toFixed(1)}°C` : '—');
    setVal('weather-wind',
        weather.wind_speed != null ? `${Number(weather.wind_speed).toFixed(1)} km/h` : '—');
    setVal('weather-humidity',
        weather.humidity != null ? `${Number(weather.humidity).toFixed(0)}%` : '—');
}

// ──────────────── Reasons ────────────────
function updateReasons(reasons) {
    const list = document.getElementById('reasons-list');
    if (!reasons || reasons.length === 0) {
        list.innerHTML = '<li class="reason-item">No significant risk factors detected.</li>';
        return;
    }
    list.innerHTML = reasons.map((reason, i) =>
        `<li class="reason-item" style="animation-delay: ${i * 0.1}s">${escapeHtml(reason)}</li>`
    ).join('');
}

// ──────────────── Segments ────────────────
function updateSegments(segments) {
    const container = document.getElementById('segments-list');
    if (!segments || segments.length === 0) {
        container.innerHTML = '<p style="color:var(--text-secondary);font-size:0.88rem;">No segment data available.</p>';
        return;
    }

    const classMap = { 0: 'safe', 1: 'caution', 2: 'danger' };

    container.innerHTML = segments.map((seg, i) => {
        const riskClass = classMap[seg.risk_level] || 'safe';
        return `
            <div class="segment-card segment-${riskClass}" style="animation-delay: ${i * 0.12}s">
                <div class="segment-route">
                    <span class="segment-from">${escapeHtml(seg.from.name)}</span>
                    <span class="segment-arrow">→</span>
                    <span class="segment-to">${escapeHtml(seg.to.name)}</span>
                </div>
                <div class="segment-meta">
                    <span class="badge badge-${riskClass}">${escapeHtml(seg.risk_label)}</span>
                    <span class="segment-distance">${seg.length_km} km</span>
                </div>
            </div>
        `;
    }).join('');
}

// ──────────────── Draw Route on Map ────────────────
function drawRouteOnMap(data) {
    routeLayer.clearLayers();
    markerLayer.clearLayers();

    if (!data.segments || data.segments.length === 0) return;

    const riskColors = { 0: '#10b981', 1: '#f59e0b', 2: '#ef4444' };
    const bounds = [];

    data.segments.forEach((seg, i) => {
        const latlngs = [
            [seg.from.lat, seg.from.lng],
            [seg.to.lat, seg.to.lng]
        ];
        bounds.push(...latlngs);

        // Route polyline
        const polyline = L.polyline(latlngs, {
            color: riskColors[seg.risk_level] || '#06b6d4',
            weight: 5,
            opacity: 0.9,
            dashArray: seg.risk_level === 2 ? '10, 10' : null,
            lineCap: 'round',
            lineJoin: 'round'
        });

        polyline.bindPopup(`
            <div style="font-family:Inter,sans-serif;padding:4px;min-width:140px;">
                <strong>${escapeHtml(seg.from.name)} → ${escapeHtml(seg.to.name)}</strong><br>
                <span style="color:${riskColors[seg.risk_level]};font-weight:600;">Risk: ${escapeHtml(seg.risk_label)}</span><br>
                Distance: ${seg.length_km} km
            </div>
        `);

        routeLayer.addLayer(polyline);

        // From marker
        const isFirst = i === 0;
        const isLast = i === data.segments.length - 1;

        const fromMarker = L.circleMarker([seg.from.lat, seg.from.lng], {
            radius: isFirst ? 10 : 6,
            fillColor: isFirst ? '#06b6d4' : (riskColors[seg.risk_level] || '#06b6d4'),
            color: '#fff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.9
        });
        fromMarker.bindTooltip(seg.from.name, {
            permanent: true,
            direction: 'top',
            offset: [0, -10],
            className: 'city-tooltip'
        });
        markerLayer.addLayer(fromMarker);

        // To marker for last segment
        if (isLast) {
            const toMarker = L.circleMarker([seg.to.lat, seg.to.lng], {
                radius: 10,
                fillColor: '#8b5cf6',
                color: '#fff',
                weight: 2,
                opacity: 1,
                fillOpacity: 0.9
            });
            toMarker.bindTooltip(seg.to.name, {
                permanent: true,
                direction: 'top',
                offset: [0, -10],
                className: 'city-tooltip'
            });
            markerLayer.addLayer(toMarker);
        }
    });

    // Fit map to route
    if (bounds.length > 0) {
        map.fitBounds(bounds, { padding: [50, 50], maxZoom: 12 });
    }
}

// ──────────────── Route Info ────────────────
function showRouteInfo(routeInfo) {
    if (!routeInfo) return;

    const infoCard = document.getElementById('route-info');
    infoCard.classList.remove('hidden');

    const setVal = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
    };

    setVal('route-distance', routeInfo.distance_km != null ? `${routeInfo.distance_km} km` : '—');
    setVal('route-time', routeInfo.estimated_time || '—');

    const factorsEl = document.getElementById('route-factors');
    if (factorsEl && routeInfo.risk_factors) {
        factorsEl.innerHTML = routeInfo.risk_factors
            .map(f => `<span class="risk-factor-tag">${escapeHtml(f)}</span>`)
            .join('');
    }
}

// ──────────────── Notifications ────────────────
function showNotification(message, type = 'info') {
    const notif = document.createElement('div');
    notif.className = `notification notification-${type}`;

    const iconMap = {
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️',
        success: '✅'
    };

    notif.innerHTML = `
        <span class="notif-icon">${iconMap[type] || 'ℹ️'}</span>
        <span class="notif-message">${escapeHtml(message)}</span>
    `;

    document.body.appendChild(notif);

    // Trigger reflow then animate in
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            notif.classList.add('show');
        });
    });

    // Auto-dismiss after 4s
    setTimeout(() => {
        notif.classList.remove('show');
        setTimeout(() => {
            if (notif.parentNode) notif.remove();
        }, 350);
    }, 4000);
}

// ──────────────── Utilities ────────────────
function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}
