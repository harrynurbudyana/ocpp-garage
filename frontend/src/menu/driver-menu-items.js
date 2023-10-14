export const menuItems = [
  {
    name: "Drivers",
    key: "drivers",
    icon: "mdi mdi-arrow-left",
    isActive: () => true,
    getPath: ({ currentGarage }) => `${currentGarage.id}/drivers`,
  },
];
