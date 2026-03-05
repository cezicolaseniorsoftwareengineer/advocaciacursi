import { LeadRepositoryPort } from "../../ports/out/lead-repository-port.js";

const STORAGE_KEY = "advocaciaLeads";

export class LocalStorageLeadRepository extends LeadRepositoryPort {
  save(lead) {
    const stored = localStorage.getItem(STORAGE_KEY);
    const leads = stored ? JSON.parse(stored) : [];
    leads.unshift(lead);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(leads));
    return lead;
  }

  list() {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  }
}
