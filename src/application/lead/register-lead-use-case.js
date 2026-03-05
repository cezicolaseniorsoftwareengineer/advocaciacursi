import { LeadEntity } from "../../domain/lead/lead-entity.js";

export class RegisterLeadUseCase {
  constructor(leadRepository) {
    this.leadRepository = leadRepository;
  }

  execute(payload) {
    const lead = LeadEntity.create(payload);
    this.leadRepository.save(lead);
    return lead;
  }
}
