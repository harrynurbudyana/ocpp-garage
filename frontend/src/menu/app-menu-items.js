export const menuItems = [
  {
    name: "Garages",
    key: "garages",
    icon: "mdi mdi-garage-variant-lock",
    isVisible: ({ currentUser }) => currentUser.is_superuser,
    getPath: () => "/garages",
  },
  {
    name: "Stations",
    key: "stations",
    icon: "mdi mdi-ev-station",
    isVisible: ({ currentGarage }) => !!currentGarage,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/stations`,
  },
  {
    name: "Drivers",
    key: "drivers",
    icon: "mdi mdi-card-account-details-outline",
    isVisible: ({ currentGarage }) => !!currentGarage,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/drivers`,
  },
  {
    name: "Operators",
    key: "drivers",
    icon: "mdi mdi-account-tie",
    isVisible: ({ currentUser, currentGarage }) =>
      !!currentGarage && currentUser.is_superuser,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/operators`,
  },
  {
    name: "Transactions",
    key: "transactions",
    icon: "mdi mdi-battery-charging-high",
    isVisible: ({ currentGarage }) => !!currentGarage,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/transactions`,
  },
];
