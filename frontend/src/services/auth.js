import { request } from "@/api";
import router from "@/router";

const { currentRoute } = router;

export function inviteUser(data) {
  return request.post(`/${currentRoute.value.params.garageId}/invite`, data);
}
