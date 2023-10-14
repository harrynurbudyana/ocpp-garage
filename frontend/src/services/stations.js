import { request } from "@/api";
import { useRoute } from "vue-router";

const endpoint = "charge_points";

export function deleteStation(stationId) {
  const { params } = useRoute();
  return request.delete(`/${params.garageId}/${endpoint}/${stationId}`);
}

export function addStation(data) {
  const { params } = useRoute();
  return request.post(`/${params.garageId}/${endpoint}/`, data);
}

export function listStations(queryParams) {
  let searchParams = new URLSearchParams(queryParams);
  const { params } = useRoute();
  return request.get(
    `/${params.garageId}/${endpoint}/?${searchParams.toString()}`
  );
}

export function listSimpleStations() {
  const { params } = useRoute();
  return request.get(`/${params.garageId}/${endpoint}/autocomplete/`);
}

export function getStation(stationId) {
  const { params } = useRoute();
  return request.get(`/${params.garageId}/${endpoint}/${stationId}`);
}

export function updateStation(stationId, data) {
  const { params } = useRoute();
  return request.put(`/${params.garageId}/${endpoint}/${stationId}`, data);
}

export function updateConnector({ stationId, connectorId }) {
  const { params } = useRoute();
  return request.put(
    `/${params.garageId}/${endpoint}/${stationId}/connectors/${connectorId}`
  );
}

export function softResetStation(stationId) {
  const { params } = useRoute();
  return request.patch(`/${params.garageId}/${endpoint}/${stationId}`);
}
