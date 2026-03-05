export function validateLeadPayload(payload) {
  const requiredFields = ["nome", "email", "telefone", "mensagem"];
  return requiredFields.every((field) => {
    const value = payload[field];
    return typeof value === "string" && value.trim().length > 0;
  });
}
