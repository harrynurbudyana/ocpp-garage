import { request } from "@/api";
import router from "@/router";

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
