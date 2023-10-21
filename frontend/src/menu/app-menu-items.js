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
    key: "operators",
    icon: "mdi mdi-account-tie",
    isVisible: ({ currentUser, currentGarage }) =>
      !!currentGarage && currentUser.is_superuser,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/operators`,
  },
  {
    name: "Government Rebates",
    key: "government-rebates",
    icon: "mdi mdi-cash-refund",
    isVisible: ({ currentGarage }) => !!currentGarage,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/government-rebates`,
  },
  {
    name: "Transactions",
    key: "transactions",
    icon: "mdi mdi-battery-charging-high",
    isVisible: ({ currentGarage }) => !!currentGarage,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/transactions`,
  },
  {
    name: "Settings",
    key: "settings",
    icon: "mdi mdi-tune",
    isVisible: ({ currentGarage }) => !!currentGarage,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/settings`,
  },
];
