import { request } from "@/api";
import router from "@/router";

const { currentRoute } = router;

const endpoint = "government-rebates";

export function listRebatesPeriods() {
  return request.get(
    `/${currentRoute.value.params.garageId}/${endpoint}/periods`
  );
}

export function listGovernmentRebates(params) {
  let searchParams = new URLSearchParams(params);
  return request.get(
    `/${
      currentRoute.value.params.garageId
    }/${endpoint}/?${searchParams.toString()}`
  );
}

export function addGovernmentRebate(data) {
  return request.post(
    `/${currentRoute.value.params.garageId}/${endpoint}/`,
    data
  );
}

export function deleteGovernmentRebate(rebateId) {
  return request.delete(
    `/${currentRoute.value.params.garageId}/${endpoint}/${rebateId}`
  );
}

export function editGovernmentRebate(rebateId, data) {
  return request.put(
    `/${currentRoute.value.params.garageId}/${endpoint}/${rebateId}`,
    data
  );
}
