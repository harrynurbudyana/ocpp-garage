export const DATETIME_FORMAT = "MMM DD, YYYY, hh:mm A";

export const EVENT_NAMES = {
  status_notification: "StatusNotification",
  lost_connection: "lost_connection",
  heartbeat: "Heartbeat",
  start_transaction: "StartTransaction",
  stop_transaction: "StopTransaction",
};

export const STATION_STATUS = {
  available: "Available",
  unavailable: "Unavailable",
  faulted: "Faulted",
  preparing: "Preparing",
  charging: "Charging",
  suspendedEVSE: "SuspendedEVSE",
  suspendedEV: "SuspendedEV",
  finishing: "Finishing",
};

export const TRANSACTION_STATUS = {
  completed: "completed",
  in_progress: "in progress",
};

export const STATION_STATUS_COLOR = {
  available: "#8cef91",
  unavailable: "#7e817d",
  faulted: "#DC184CFF",
  preparing: "#efc909",
  charging: "#0ccaec",
};

export const TRANSACTION_STATUS_COLOR = {
  in_progress: "#0ee018",
  completed: "#7e817d",
};

export const DRIVERS_STATUS = {
  true: "#0ee018",
  false: "#DC184CFF",
};
