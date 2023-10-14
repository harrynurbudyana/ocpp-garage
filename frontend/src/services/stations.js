import { request } from "@/api";
import router from "@/router";

const { currentRoute } = router;

const endpoint = "charge_points";

export function deleteStation(stationId) {
  return request.delete(
    `/${currentRoute.value.params.garageId}/${endpoint}/${stationId}`
  );
}

export function addStation(data) {
  return request.post(
    `/${currentRoute.value.params.garageId}/${endpoint}/`,
    data
  );
}

export function listStations(queryParams) {
  let searchParams = new URLSearchParams(queryParams);
  return request.get(
    `/${
      currentRoute.value.params.garageId
    }/${endpoint}/?${searchParams.toString()}`
  );
}

export function listSimpleStations() {
  return request.get(
    `/${currentRoute.value.params.garageId}/${endpoint}/autocomplete/`
  );
}

export function getStation(stationId) {
  return request.get(
    `/${currentRoute.value.params.garageId}/${endpoint}/${stationId}`
  );
}

export function updateStation(stationId, data) {
  return request.put(
    `/${currentRoute.value.params.garageId}/${endpoint}/${stationId}`,
    data
  );
}

export function updateConnector({ stationId, connectorId }) {
  return request.put(
    `/${currentRoute.value.params.garageId}/${endpoint}/${stationId}/connectors/${connectorId}`
  );
}

export function softResetStation(stationId) {
  return request.patch(
    `/${currentRoute.value.params.garageId}/${endpoint}/${stationId}`
  );
}
