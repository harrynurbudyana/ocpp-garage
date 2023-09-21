import { request } from "@/api";

const endpoint = "drivers";

export function deleteDriver(driverId) {
  return request.delete(`/${endpoint}/${driverId}`);
}

export function addDriver(data) {
  return request.post(`/${endpoint}`, data);
}

export function listDrivers(arg) {
  let { page = 1 } = arg || {};
  let { search = "" } = arg || {};
  return request.get(`/${endpoint}?page=${page}&search=${search}`);
}

export function getDriver(driverId) {
  return request.get(`/${endpoint}/${driverId}`);
}

export function updateDriver(driverId, data) {
  return request.put(`/${endpoint}/${driverId}`, data);
}
