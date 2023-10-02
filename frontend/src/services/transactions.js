import { request } from "@/api";

const endpoint = "transactions";

export function listTransactions(arg) {
  let { page = 1 } = arg || {};
  let { search = "" } = arg || {};
  return request.get(`/${endpoint}?page=${page}&search=${search}`);
}

export function remoteStartTransaction(data) {
  return request.post(`/${endpoint}`, data);
}

export function remoteStopTransaction(transactionId) {
  return request.put(`/${endpoint}/${transactionId}`);
}