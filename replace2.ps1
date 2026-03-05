$html = Get-Content index.html -Raw -Encoding UTF8

$newSobre = @'
        <!-- ============================================================
         SOBRE
         ============================================================ -->
        <section id="sobre" class="section" style="background: linear-gradient(180deg, var(--bg-secondary) 0%, rgba(8,12,23,0.95) 100%); position: relative; border-top: 1px solid rgba(199,168,107,0.1); border-bottom: 1px solid rgba(199,168,107,0.1); overflow: hidden;">
            <div style="position: absolute; top: 50%; right: -10%; width: 600px; height: 600px; background: radial-gradient(circle, rgba(199,168,107,0.06) 0%, transparent 60%); transform: translateY(-50%); pointer-events: none;"></div>
            
            <div class="container" style="position: relative; z-index: 1;">
                <div class="sobre__grid">
                    
                    <div class="sobre__image-container">
                        <img src="https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&w=800&auto=format&fit=crop" alt="Advocacia de Elite">
                        <div class="sobre__badge">
                            <div style="font-size: 2.5rem; line-height: 1; letter-spacing: -2px;">+10</div>
                            <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.2rem;">Anos de<br>Alta Performance</div>
                        </div>
                    </div>

                    <div class="sobre__content" style="padding-top: 2rem;">
                        <div style="display: inline-block; padding: 0.4rem 1.2rem; border-radius: 50px; background: rgba(199,168,107,0.1); border: 1px solid rgba(199,168,107,0.2); color: var(--accent-gold); font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1.5rem;">Sócio Majoritário</div>
                        
                        <h2 style="font-size: clamp(2rem, 4vw, 3.5rem); line-height: 1.1; margin-bottom: 1.5rem;">
                            Sobre <span class="accent-gold" style="display: block; margin-top: 0.5rem;">Dr. Estevão Cursi</span>
                        </h2>
                        
                        <div style="width: 60px; height: 4px; background: var(--accent-gold); border-radius: 2px; margin-bottom: 2rem;"></div>
                        
                        <p style="font-size: 1.15rem; line-height: 1.8; color: var(--text-secondary); margin-bottom: 1.5rem;">
                            Atuação lapidada ao longo de uma carreira sólida, combinando <strong>dogmática rigorosa</strong> e <strong>inteligência estratégica</strong> para proporcionar resoluções definitivas em contenciosos de alta complexidade.
                        </p>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin: 2.5rem 0;">
                            <div style="background: rgba(22, 37, 59, 0.4); border: 1px solid rgba(199, 168, 107, 0.1); padding: 1.5rem; border-radius: var(--radius-sm); border-left: 2px solid var(--accent-blue);">
                                <h4 style="color: var(--text-primary); margin-bottom: 0.5rem; font-family: var(--font-heading);">Boutique Jurídica</h4>
                                <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; margin: 0;">Atendimento hipercristalizado onde cada cliente é tratado como um projeto vital exclusivo.</p>
                            </div>
                            <div style="background: rgba(22, 37, 59, 0.4); border: 1px solid rgba(199, 168, 107, 0.1); padding: 1.5rem; border-radius: var(--radius-sm); border-left: 2px solid var(--accent-gold);">
                                <h4 style="color: var(--text-primary); margin-bottom: 0.5rem; font-family: var(--font-heading);">Tratamento Tático</h4>
                                <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; margin: 0;">Uso de ferramentas digitais como o IDPJ para reaver créditos massivos e devassa patrimonial.</p>
                            </div>
                        </div>

                        <blockquote style="border-left: 3px solid var(--accent-gold); padding-left: 1.5rem; margin-top: 2.5rem;">
                            <p style="font-size: 1.3rem; line-height: 1.6; color: var(--accent-gold); font-family: var(--font-heading); font-style: italic; margin: 0;">
                                "Compromisso inquebrável com a ética corporativa, a precisão material e a garantia irrestrita dos direitos fundamentais."
                            </p>
                        </blockquote>
                    </div>
                </div>
            </div>
        </section>
'@

$html = $html -replace '(?s)<!-- ============================================================\s*SOBRE.*?</section>', $newSobre
Set-Content index.html -Value $html -Encoding UTF8
