export const menuItems = [
  {
    name: "Garages",
    key: "Garages",
    icon: "mdi mdi-garage-variant-lock",
    isVisible: ({ currentUser }) => currentUser.is_superuser,
    getPath: () => "/garages",
  },
  {
    name: "Stations",
    key: "Stations",
    icon: "mdi mdi-ev-station",
    isVisible: ({ currentGarage }) => !!currentGarage,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/stations`,
  },
  {
    name: "Users",
    key: "Users",
    icon: "mdi mdi-account-tie",
    isVisible: ({ currentUser, currentGarage }) =>
      !!currentGarage && (currentUser.is_superuser || currentUser.is_admin),
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/users`,
  },
  {
    name: "Transactions",
    key: "Transactions",
    icon: "mdi mdi-battery-charging-high",
    isVisible: ({ currentGarage }) => !!currentGarage,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/transactions`,
  },
  {
    name: "Settings",
    key: "Settings",
    icon: "mdi mdi-tune",
    isVisible: ({ currentGarage, currentUser }) =>
      !!currentGarage && (currentUser.is_superuser || currentUser.is_admin),
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/settings`,
  },
];
