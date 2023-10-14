import { request } from "@/api";
import { useRoute } from "vue-router";

const endpoint = "charge_points";

export function deleteStation(stationId) {
  return request.delete(`/${endpoint}/${stationId}`);
}

export function addStation(data) {
  return request.post(`/${endpoint}/`, data);
}

export function listStations(queryParams) {
  let searchParams = new URLSearchParams(queryParams);
  const { params } = useRoute();
  return request.get(
    `/${params.garageId}/${endpoint}/?${searchParams.toString()}`
  );
}

export function listSimpleStations() {
  return request.get(`/${endpoint}/autocomplete/`);
}

export function getStation(stationId) {
  return request.get(`/${endpoint}/${stationId}`);
}

export function updateStation(stationId, data) {
  return request.put(`/${endpoint}/${stationId}`, data);
}

export function updateConnector({ stationId, connectorId }) {
  return request.put(`/${endpoint}/${stationId}/connectors/${connectorId}`);
}

export function softResetStation(stationId) {
  return request.patch(`/${endpoint}/${stationId}`);
}
