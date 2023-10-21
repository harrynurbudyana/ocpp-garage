import { request } from "@/api";
import router from "@/router";

const { currentRoute } = router;

const endpoint = "garages";

export function addGarage(data) {
  return request.post(`/${endpoint}`, data);
}

export function listGarages(params) {
  let searchParams = new URLSearchParams(params);
  return request.get(`/${endpoint}/?${searchParams.toString()}`);
}

export function getGarage(garageId) {
  return request.get(`${endpoint}/${garageId}`);
}

export function getGarageRates() {
  return request.get(`${endpoint}/${currentRoute.value.params.garageId}/rates`);
}

export function saveSettings(data) {
  return request.post(
    `${endpoint}/${currentRoute.value.params.garageId}/settings`,
    data
  );
}
