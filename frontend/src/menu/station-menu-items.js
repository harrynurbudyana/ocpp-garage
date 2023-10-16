export const menuItems = [
  {
    name: "Stations",
    key: "stations",
    icon: "mdi mdi-arrow-left",
    isVisible: () => true,
    getPath: ({ currentGarage }) => `/${currentGarage.id}/stations`,
  },
];
