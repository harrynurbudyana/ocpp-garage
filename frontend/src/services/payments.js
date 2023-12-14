import { request } from "@/api";

export function requestCheckoutSession(data) {
  return request.post("/payments/checkout", data);
}
