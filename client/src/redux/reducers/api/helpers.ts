export const addAuthHeader = (headers: Headers) => {
  headers.set("Authorization", `Bearer ${localStorage.authToken}`);
  return headers;
};
