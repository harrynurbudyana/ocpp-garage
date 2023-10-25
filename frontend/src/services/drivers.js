import { request } from "@/api";
import router from "@/router";

const API_URL = import.meta.env.VITE_API_URL.trim("/");

const { currentRoute } = router;

const endpoint = "drivers";

export function deleteDriver(driverId) {
  return request.delete(
    `/${currentRoute.value.params.garageId}/${endpoint}/${driverId}`
  );
}

export function addDriver(data) {
  return request.post(
    `/${currentRoute.value.params.garageId}/${endpoint}/`,
    data
  );
}

export function listDrivers(params) {
  let searchParams = new URLSearchParams(params);
  return request.get(
    `/${
      currentRoute.value.params.garageId
    }/${endpoint}/?${searchParams.toString()}`
  );
}

export function getDriver(driverId) {
  return request.get(
    `/${currentRoute.value.params.garageId}/${endpoint}/${driverId}`
  );
}

export function requestDriversReport(driverId) {
  const link = document.createElement("a");
  link.href = `${API_URL}/${currentRoute.value.params.garageId}/${endpoint}/${driverId}/statement`;

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

export function updateDriver(driverId, data) {
  return request.put(
    `/${currentRoute.value.params.garageId}/${endpoint}/${driverId}`,
    data
  );
}

export function releaseStation({ driverId, stationId }) {
  return request.delete(
    `/${currentRoute.value.params.garageId}/${endpoint}/${driverId}/charge_points/${stationId}/`
  );
}
