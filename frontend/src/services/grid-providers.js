import { request } from "@/api";

const endpoint = "grid-providers";

export function listGridProviders(params) {
  let searchParams = new URLSearchParams(params);
  return request.get(`/${endpoint}/?${searchParams.toString()}`);
}
