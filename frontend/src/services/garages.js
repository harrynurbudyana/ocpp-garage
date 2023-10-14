import { request } from "@/api";

const endpoint = "garages";

export function addGarage(data) {
  return request.post(`/${endpoint}`, data);
}

export function listGarages(params) {
  let searchParams = new URLSearchParams(params);
  return request.get(`/${endpoint}/?${searchParams.toString()}`);
}
