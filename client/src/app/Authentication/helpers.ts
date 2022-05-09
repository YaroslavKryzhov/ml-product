export const passwordValidate = (val: string) =>
  !val.length ||
  (/^[a-zA-Z0-9_.!=-]{6,}$/g.test(val) &&
    /[a-z]/g.test(val) &&
    /[A-Z]/g.test(val) &&
    /[0-9]/g.test(val) &&
    /[_.!=-]/g.test(val));
