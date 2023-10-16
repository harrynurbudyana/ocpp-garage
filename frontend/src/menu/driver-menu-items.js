export const menuItems = [
  {
    name: "Drivers",
    key: "drivers",
    icon: "mdi mdi-arrow-left",
    isVisible: () => true,
    getPath: ({ currentGarage }) => `/${currentGarage.id}/drivers`,
  },
];
