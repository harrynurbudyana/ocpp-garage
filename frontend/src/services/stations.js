import { request } from "@/api";

const endpoint = "charge_points";

export function deleteStation(stationId) {
  return request.delete(`/${endpoint}/${stationId}`);
}

export function addStation(data) {
  return request.post(`/${endpoint}`, data);
}

export function listStations(arg) {
  let { page = 1 } = arg || {};
  let { search = "" } = arg || {};
  return request.get(`/${endpoint}?page=${page}&search=${search}`);
}

export function listSimpleStations() {
  return request.get(`/${endpoint}/autocomplete`);
}

export function getStation(stationId) {
  return request.get(`/${endpoint}/${stationId}`);
}

export function updateStation(stationId, data) {
  return request.put(`/${endpoint}/${stationId}`, data);
}
