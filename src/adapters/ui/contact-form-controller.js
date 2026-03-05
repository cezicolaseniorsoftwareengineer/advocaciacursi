import { RegisterLeadUseCase } from "../../application/lead/register-lead-use-case.js";
import { LocalStorageLeadRepository } from "../persistence/local-storage-lead-repository.js";

export class ContactFormController {
  constructor() {
    this.useCase = new RegisterLeadUseCase(new LocalStorageLeadRepository());
  }

  register(payload) {
    return this.useCase.execute(payload);
  }
}
