import { Role } from "@/components/enums";

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
    name: "Statements",
    key: "statements",
    icon: "mdi mdi-receipt-text-outline",
    isVisible: ({ currentGarage, currentUser }) =>
      !!currentGarage && currentUser.role === Role.resident,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/statements`,
  },
  {
    name: "Residents",
    key: "residents",
    icon: "mdi mdi-card-account-details-outline",
    isVisible: ({ currentGarage, currentUser }) =>
      !!currentGarage && currentUser.role !== Role.resident,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/residents`,
  },
  {
    name: "Managers",
    key: "employees",
    icon: "mdi mdi-account-tie",
    isVisible: ({ currentUser, currentGarage }) =>
      !!currentGarage && currentUser.is_superuser,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/managers`,
  },
  {
    name: "Government Rebates",
    key: "government-rebates",
    icon: "mdi mdi-cash-refund",
    isVisible: ({ currentGarage, currentUser }) =>
      !!currentGarage && currentUser.is_superuser,
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/government-rebates`,
  },
  {
    name: "Transactions",
    key: "transactions",
    icon: "mdi mdi-battery-charging-high",
    isVisible: ({ currentGarage, currentUser }) =>
      !!currentGarage && currentUser.role !== "resident",
    getPath: ({ currentGarage }) => `/${currentGarage?.id}/transactions`,
  },
];
