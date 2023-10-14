export const menuItems = [
  {
    name: "Garages",
    key: "garages",
    icon: "mdi mdi-garage-variant-lock",
    isActive: ({ currentUser }) => currentUser.is_superuser,
    getPath: () => "/garages",
  },
  {
    name: "Stations",
    key: "stations",
    icon: "mdi mdi-ev-station",
    isActive: ({ currentGarage }) => !!currentGarage,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/stations`,
  },
  {
    name: "Drivers",
    key: "drivers",
    icon: "mdi mdi-account-circle",
    isActive: ({ currentGarage }) => !!currentGarage,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/drivers`,
  },
  {
    name: "Transactions",
    key: "transactions",
    icon: "mdi mdi-battery-charging-high",
    isActive: ({ currentGarage }) => !!currentGarage,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/transactions`,
  },
];
