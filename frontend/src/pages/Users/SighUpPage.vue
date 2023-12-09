<template>
  <v-form v-model="isValid">
    <v-container>
      <v-row justify="center" class="mt-16">
        <v-card width="600">
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    label="First Name"
                    required
                    :rules="rules.driver.firstNameRules"
                    v-model="data.first_name"
                    density="compact"
                    variant="underlined"
                    validate-on="lazy blur"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    label="Last Name"
                    required
                    :rules="rules.driver.lastNameRules"
                    v-model="data.last_name"
                    density="compact"
                    variant="underlined"
                    validate-on="lazy blur"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    label="Address"
                    required
                    :rules="rules.driver.addressRules"
                    v-model="data.address"
                    density="compact"
                    variant="underlined"
                    @input="clearError"
                    validate-on="lazy blur"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    type="password"
                    label="Password"
                    required
                    :rules="rules.driver.passwordRules"
                    v-model="data.password"
                    density="compact"
                    variant="underlined"
                    @input="clearError"
                    validate-on="lazy blur"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    type="password"
                    label="Confirm password"
                    required
                    :rules="[
                      (v) =>
                        v !== data.password ? 'Passwords do not match.' : true,
                    ]"
                    v-model="data.confirm_password"
                    density="compact"
                    variant="underlined"
                    @input="clearError"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions class="mb-7">
            <v-spacer></v-spacer>

            <v-btn
              color="blue-darken-1"
              variant="text"
              @click="onSubmit"
              :loading="loading"
              :disabled="!isValid || loading"
            >
              Confirm
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-row>
    </v-container>
  </v-form>
</template>
<script setup>
import { onMounted, ref } from "vue";
import { rules } from "@/configs/validation";
import { useRouter } from "vue-router";
import { addUser, checkInvitationLink } from "@/services/users";

const router = useRouter();
const loading = ref(false);
const isValid = ref(false);
const data = ref({});
const errors = ref({});
const showError = ref(false);

const onSubmit = () => {
  loading.value = true;
  let garageId = data.value.garage_id;
  delete data.value.garageId;
  delete data.value.confirm_password;
  addUser({ garageId, data: data.value })
    .then(() => {
      router.push({ name: "Login" });
    })
    .finally(() => {
      loading.value = false;
    });
};

const clearError = () => {
  showError.value = false;
  errors.value = {};
};

onMounted(() => {
  let userId = router.currentRoute.value.params.userId;
  checkInvitationLink(userId).then((response) => (data.value = response));
});
</script>
