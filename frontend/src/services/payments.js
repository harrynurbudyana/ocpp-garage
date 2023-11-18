import { request } from "@/api";

const endpoint = "payments";

export function verifyPayment(token) {
  return request.get(`/${endpoint}/${token}`);
}

export function createPaymentSession(data) {
  return request.post(`/${endpoint}/session`, data);
}

export function confirmPayment(data) {
  return request.post(`/${endpoint}`, data);
}
