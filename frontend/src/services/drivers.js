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

export function addDriver({ garageId, data }) {
  return request.post(`/${garageId}/${endpoint}`, data);
}

export function checkInvitationLink(userId) {
  return request.get(`/${endpoint}/signup/${userId}`);
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

export function requestDriversReport({ driverId, month, year }) {
  const link = document.createElement("a");
  link.href = `${API_URL}/${currentRoute.value.params.garageId}/${endpoint}/${driverId}/statement?month=${month}&year=${year}`;
  link.target = "_blank";

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

export function releaseStation({ driverId, stationId, connectorId }) {
  return request.delete(
    `/${currentRoute.value.params.garageId}/${endpoint}/${driverId}/charge_points/${stationId}/connectors/${connectorId}`
  );
}
