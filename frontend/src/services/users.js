import { request } from "@/api";
import router from "@/router";

const { currentRoute } = router;

const endpoint = "users";

export function listUsers(params) {
  let searchParams = new URLSearchParams(params);
  return request.get(
    `/${
      currentRoute.value.params.garageId
    }/${endpoint}?${searchParams.toString()}`
  );
}

export function addUser({ garageId, data }) {
  return request.post(`/${garageId}/${endpoint}`, data);
}

export function inviteUser(data) {
  return request.post(`/${currentRoute.value.params.garageId}/invite`, data);
}

export function checkInvitationLink(userId) {
  return request.get(`/${endpoint}/signup/${userId}`);
}
