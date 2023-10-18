import { request } from "@/api";

const endpoint = "actions";

export function listActions(params) {
  const { garageId } = params;
  delete params["garageId"];
  let searchParams = new URLSearchParams(params);
  return request.get(`/${endpoint}/${garageId}?${searchParams.toString()}`);
}
