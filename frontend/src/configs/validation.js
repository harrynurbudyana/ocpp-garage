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
  this.emailRegex =
    /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
  this.maxFirstNameLength = 15;
  this.maxLastNameLength = 15;

  this.maxGarageNameLength = 15;
  this.macGarageContactLength = 25;
  this.maxPhoneLength = 15;
  this.maxProviderName = 15;
  this.maxCityLength = 15;
  this.maxPostNummerLength = 4;

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
    cityRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxCityLength) {
          return `Maximum ${this.maxCityLength} characters required`;
        }
        return true;
      },
    ],
    streetRules: [
      ...this.common,
      (value) => {
        if (value?.length > this.maxAddressLength) {
          return `Maximum ${this.maxAddressLength} characters required`;
        }
        return true;
      },
    ],
    emailRules: [
      ...this.common,
      (value) => {
        if (!this.emailRegex.test(value)) {
          return "Invalid email format.";
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
        const regex =
          /^(\+{0,})(\d{0,})([(]{1}\d{1,3}[)]{0,}){0,}(\s?\d+|\+\d{2,3}\s{1}\d+|\d+){1}[\s|-]?\d+([\s|-]?\d+){1,2}(\s){0,}$/gm;
        if (!regex.test(value)) {
          return "Invalid phone number format.";
        }
        return true;
      },
    ],
    postNummerRules: [
      ...this.common,
      (value) => {
        if (!/^\d+$/.test(value)) {
          return "Only digits required.";
        }
        return true;
      },
      (value) => {
        if (value?.length !== this.maxPostNummerLength) {
          return `${this.maxPostNummerLength} characters required`;
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
        if (!this.emailRegex.test(value)) {
          return "Invalid email format.";
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
