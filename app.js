// Vancouver coordinates
const LAT = 49.2827;
const LON = -123.1207;

const WEATHER_CODES = {
  0: { description: "Clear sky", icon: "\u2600\ufe0f" },
  1: { description: "Mainly clear", icon: "\ud83c\udf24\ufe0f" },
  2: { description: "Partly cloudy", icon: "\u26c5" },
  3: { description: "Overcast", icon: "\u2601\ufe0f" },
  45: { description: "Foggy", icon: "\ud83c\udf2b\ufe0f" },
  48: { description: "Depositing rime fog", icon: "\ud83c\udf2b\ufe0f" },
  51: { description: "Light drizzle", icon: "\ud83c\udf26\ufe0f" },
  53: { description: "Moderate drizzle", icon: "\ud83c\udf26\ufe0f" },
  55: { description: "Dense drizzle", icon: "\ud83c\udf26\ufe0f" },
  56: { description: "Light freezing drizzle", icon: "\ud83c\udf27\ufe0f" },
  57: { description: "Dense freezing drizzle", icon: "\ud83c\udf27\ufe0f" },
  61: { description: "Slight rain", icon: "\ud83c\udf27\ufe0f" },
  63: { description: "Moderate rain", icon: "\ud83c\udf27\ufe0f" },
  65: { description: "Heavy rain", icon: "\ud83c\udf27\ufe0f" },
  66: { description: "Light freezing rain", icon: "\ud83c\udf27\ufe0f" },
  67: { description: "Heavy freezing rain", icon: "\ud83c\udf27\ufe0f" },
  71: { description: "Slight snowfall", icon: "\ud83c\udf28\ufe0f" },
  73: { description: "Moderate snowfall", icon: "\ud83c\udf28\ufe0f" },
  75: { description: "Heavy snowfall", icon: "\ud83c\udf28\ufe0f" },
  77: { description: "Snow grains", icon: "\ud83c\udf28\ufe0f" },
  80: { description: "Slight rain showers", icon: "\ud83c\udf26\ufe0f" },
  81: { description: "Moderate rain showers", icon: "\ud83c\udf27\ufe0f" },
  82: { description: "Violent rain showers", icon: "\ud83c\udf27\ufe0f" },
  85: { description: "Slight snow showers", icon: "\ud83c\udf28\ufe0f" },
  86: { description: "Heavy snow showers", icon: "\ud83c\udf28\ufe0f" },
  95: { description: "Thunderstorm", icon: "\u26c8\ufe0f" },
  96: { description: "Thunderstorm with slight hail", icon: "\u26c8\ufe0f" },
  99: { description: "Thunderstorm with heavy hail", icon: "\u26c8\ufe0f" },
};

function getWeatherInfo(code) {
  return WEATHER_CODES[code] || { description: "Unknown", icon: "\u2753" };
}

function formatTime(isoString) {
  const date = new Date(isoString);
  return date.toLocaleTimeString("en-CA", { hour: "numeric", hour12: true });
}

function formatDay(isoString) {
  const date = new Date(isoString + "T00:00:00");
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);

  if (date.toDateString() === today.toDateString()) return "Today";
  if (date.toDateString() === tomorrow.toDateString()) return "Tomorrow";

  return date.toLocaleDateString("en-CA", { weekday: "short", month: "short", day: "numeric" });
}

function showError(message) {
  const banner = document.getElementById("error-banner");
  const msg = document.getElementById("error-message");
  msg.textContent = message;
  banner.classList.remove("hidden");
}

function hideError() {
  document.getElementById("error-banner").classList.add("hidden");
}

function renderCurrentWeather(current) {
  const info = getWeatherInfo(current.weather_code);

  document.getElementById("current-icon").textContent = info.icon;
  document.getElementById("current-temp").textContent = Math.round(current.temperature_2m);
  document.getElementById("weather-description").textContent = info.description;
  document.getElementById("feels-like").textContent = Math.round(current.apparent_temperature) + "\u00b0C";
  document.getElementById("humidity").textContent = current.relative_humidity_2m + "%";
  document.getElementById("wind").textContent = Math.round(current.wind_speed_10m) + " km/h";

  const uvEl = document.getElementById("uv-index");
  if (current.uv_index !== undefined) {
    uvEl.textContent = current.uv_index.toFixed(1);
  }

  document.getElementById("precipitation").textContent = current.precipitation + " mm";

  const visEl = document.getElementById("visibility");
  if (current.visibility !== undefined) {
    visEl.textContent = (current.visibility / 1000).toFixed(0) + " km";
  }

  document.getElementById("loading").classList.add("hidden");
  document.getElementById("current-content").classList.remove("hidden");
}

function renderHourlyForecast(hourly) {
  const container = document.getElementById("hourly-forecast");
  container.innerHTML = "";

  const now = new Date();
  const currentHourIndex = hourly.time.findIndex((t) => new Date(t) >= now);
  const startIndex = Math.max(0, currentHourIndex);
  const endIndex = Math.min(startIndex + 24, hourly.time.length);

  for (let i = startIndex; i < endIndex; i++) {
    const info = getWeatherInfo(hourly.weather_code[i]);
    const isNow = i === startIndex;

    const item = document.createElement("div");
    item.className = "hourly-item" + (isNow ? " now" : "");
    item.innerHTML =
      '<div class="hourly-time">' + (isNow ? "Now" : formatTime(hourly.time[i])) + "</div>" +
      '<div class="hourly-icon">' + info.icon + "</div>" +
      '<div class="hourly-temp">' + Math.round(hourly.temperature_2m[i]) + "\u00b0</div>";

    container.appendChild(item);
  }
}

function renderDailyForecast(daily) {
  const container = document.getElementById("daily-forecast");
  container.innerHTML = "";

  for (let i = 0; i < daily.time.length; i++) {
    const info = getWeatherInfo(daily.weather_code[i]);

    const item = document.createElement("div");
    item.className = "daily-item";
    item.innerHTML =
      '<div class="daily-day">' + formatDay(daily.time[i]) + "</div>" +
      '<div class="daily-icon">' + info.icon + "</div>" +
      '<div class="daily-temps">' +
        '<span class="daily-high">' + Math.round(daily.temperature_2m_max[i]) + "\u00b0</span>" +
        '<span class="daily-low">' + Math.round(daily.temperature_2m_min[i]) + "\u00b0</span>" +
      "</div>";

    container.appendChild(item);
  }
}

async function fetchWeather() {
  const url =
    "https://api.open-meteo.com/v1/forecast?" +
    "latitude=" + LAT +
    "&longitude=" + LON +
    "&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,uv_index,visibility" +
    "&hourly=temperature_2m,weather_code" +
    "&daily=weather_code,temperature_2m_max,temperature_2m_min" +
    "&timezone=America/Vancouver" +
    "&forecast_days=7";

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error("Weather API returned " + response.status);
  }
  return response.json();
}

async function loadWeather() {
  try {
    hideError();
    const data = await fetchWeather();

    renderCurrentWeather(data.current);
    renderHourlyForecast(data.hourly);
    renderDailyForecast(data.daily);

    document.getElementById("last-updated").textContent =
      "Updated " + new Date().toLocaleTimeString("en-CA", { hour: "2-digit", minute: "2-digit" });
  } catch (err) {
    console.error("Failed to load weather:", err);
    showError("Unable to load weather data. Check your connection.");
  }
}

document.getElementById("retry-btn").addEventListener("click", loadWeather);

// Load on start and refresh every 10 minutes
loadWeather();
setInterval(loadWeather, 10 * 60 * 1000);
