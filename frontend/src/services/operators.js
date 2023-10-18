import { request } from "@/api";
import router from "@/router";

const { currentRoute } = router;

const endpoint = "operators";

export function listOperators(params) {
  let searchParams = new URLSearchParams(params);
  return request.get(
    `/${
      currentRoute.value.params.garageId
    }/${endpoint}/?${searchParams.toString()}`
  );
}

export function addOperator(data) {
  return request.post(
    `/${currentRoute.value.params.garageId}/${endpoint}/`,
    data
  );
}
