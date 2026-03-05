export class LeadEntity {
  constructor({
    id,
    nome,
    email,
    telefone,
    mensagem,
    area,
    status = "frio",
    data,
  }) {
    this.id = id;
    this.nome = nome;
    this.email = email;
    this.telefone = telefone;
    this.mensagem = mensagem;
    this.area = area;
    this.status = status;
    this.data = data;
  }

  static create(payload, clock = () => new Date().toISOString()) {
    return new LeadEntity({
      id: Date.now(),
      ...payload,
      status: payload.status ?? "frio",
      data: payload.data ?? clock(),
    });
  }
}
