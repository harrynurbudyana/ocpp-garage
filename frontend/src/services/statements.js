import { request } from "@/api";
import router from "@/router";

const { currentRoute } = router;

const endpoint = "statements";

export function listStatements(params) {
  let searchParams = new URLSearchParams(params);
  return request.get(
    `/${
      currentRoute.value.params.garageId
    }/${endpoint}/?${searchParams.toString()}`
  );
}
