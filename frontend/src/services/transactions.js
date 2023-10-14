import { request } from "@/api";
import router from "@/router";

const { currentRoute } = router;

const endpoint = "transactions";

export function listTransactions(params) {
  let searchParams = new URLSearchParams(params);
  return request.get(
    `/${
      currentRoute.value.params.garageId
    }/${endpoint}/?${searchParams.toString()}`
  );
}

export function remoteStartTransaction(data) {
  return request.post(
    `/${currentRoute.value.params.garageId}/${endpoint}/`,
    data
  );
}

export function remoteStopTransaction(transactionId) {
  return request.put(
    `/${currentRoute.value.params.garageId}/${endpoint}/${transactionId}`
  );
}
