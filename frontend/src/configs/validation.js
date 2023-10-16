export const rules = new (function () {
  this.maxCommentLength = 50;
  this.maxAddressLength = 48;

  this.maxIdLength = 20;
  this.maxManufacturerLength = 15;
  this.maxSerialNumberLength = 30;
  this.maxModelLength = 15;
  this.maxPasswordLength = 30;

  this.maxLoginLength = 24;

  this.minLength = 3;

  this.maxEmailLength = 25;
  this.maxFirstNameLength = 15;
  this.maxLastNameLength = 15;

  this.maxGarageNameLength = 15;
  this.macGarageContactLength = 25;
  this.maxPhoneLength = 15;
  this.maxProviderName = 15;

  this.common = [
    (value) => {
      return value ? true : "field is required.";
    },
    (value) => {
      if (value?.length < this.minLength) {
        return `Minimum ${this.minLength} characters required`;
      } else {
        return true;
      }
    },
  ];

  this.station = {
    idRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxIdLength) {
          return `Maximum ${this.maxIdLength} characters required`;
        }
        return true;
      },
    ],
    manufacturerRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxManufacturerLength) {
          return `Maximum ${this.maxManufacturerLength} characters required`;
        }
        return true;
      },
    ],
    serialNumberRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxSerialNumberLength) {
          return `Maximum ${this.maxSerialNumberLength} characters required`;
        }
        return true;
      },
    ],
    modelRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxModelLength) {
          return `Maximum ${this.maxModelLength} characters required`;
        }
        return true;
      },
    ],
    passwordRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxPasswordLength) {
          return `Maximum ${this.maxPasswordLength} characters required`;
        }
        return true;
      },
    ],
    commentRules: [
      (value) => {
        if (value?.length > this.maxCommentLength) {
          return `Maximum ${this.maxCommentLength} characters required`;
        }
        return true;
      },
    ],
  };

  this.user = {
    loginRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxLoginLength) {
          return `Maximum ${this.maxLoginLength} characters required`;
        }
        return true;
      },
    ],
    passwordRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxPasswordLength) {
          return `Maximum ${this.maxPasswordLength} characters required`;
        }
        return true;
      },
    ],
  };

  this.garage = {
    nameRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxGarageNameLength) {
          return `Maximum ${this.maxGarageNameLength} characters required`;
        }
        return true;
      },
    ],
    addressRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxAddressLength) {
          return `Maximum ${this.maxAddressLength} characters required`;
        }
        return true;
      },
    ],
    contactRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.macGarageContactLength) {
          return `Maximum ${this.macGarageContactLength} characters required`;
        }
        return true;
      },
    ],
    phoneRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxPhoneLength) {
          return `Maximum ${this.maxPhoneLength} characters required`;
        }
        return true;
      },
    ],
    providerRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxProviderName) {
          return `Maximum ${this.maxProviderName} characters required`;
        }
        return true;
      },
    ],
  };

  this.driver = {
    emailRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxEmailLength) {
          return `Maximum ${this.maxEmailLength} characters required`;
        }
        return true;
      },
    ],
    firstNameRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxFirstNameLength) {
          return `Maximum ${this.maxFirstNameLength} characters required`;
        }
        return true;
      },
    ],
    lastNameRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxLastNameLength) {
          return `Maximum ${this.maxLastNameLength} characters required`;
        }
        return true;
      },
    ],
    addressRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxAddressLength) {
          return `Maximum ${this.maxAddressLength} characters required`;
        }
        return true;
      },
    ],
  };
})();
