// Startuzeiro Hub - Aplicação Centralizada de Testes e Usabilidade

let allTools = [];
let activeTab = 'playground';
let activeFilter = 'all';
let selectedCategory = 'all';
let searchQuery = '';
let serverConnected = false;

// Inicialização
document.addEventListener('DOMContentLoaded', async () => {
    initTabs();
    await checkServerStatus();
    loadTools();
    setupFiltersAndSearch();
    setupPlaygroundForms();
});

// Checagem de conectividade com o Backend Bridge
async function checkServerStatus() {
    const statusBadge = document.getElementById('server-status-badge');
    const statusText = document.getElementById('server-status-text');
    try {
        const res = await fetch('http://localhost:5050/api/status');
        if (res.ok) {
            const data = await res.json();
            serverConnected = true;
            statusBadge.className = 'inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 glow-emerald';
            statusText.textContent = `🟢 Servidor Ativo (Porta ${data.port})`;
            return;
        }
    } catch (e) {
        // Servidor offline ou executando em modo estático (file:///)
    }
    serverConnected = false;
    statusBadge.className = 'inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/30';
    statusText.textContent = '🟡 Modo Estático (Execute "abrir_painel.bat" para testes ao vivo)';
}

// Carregar catálogo de ferramentas
function loadTools() {
    // Tenta usar TOOLS_DATA embutido se disponível
    if (typeof TOOLS_DATA !== 'undefined' && Array.isArray(TOOLS_DATA)) {
        allTools = TOOLS_DATA;
    }
    updateMetrics();
    renderToolsList();
    renderOpenSourceList();
    renderSaasList();
}

// Atualizar métricas do header
function updateMetrics() {
    const totalCount = allTools.length;
    const osCount = allTools.filter(t => t.tipo === 'open-source').length;
    const saasCount = allTools.filter(t => t.tipo && (t.tipo.includes('saas') || t.tipo.includes('web') || t.tipo.includes('banco') || t.tipo.includes('plataforma'))).length;
    const mcpCount = allTools.filter(t => t.tipo === 'mcp-servico-api').length;

    document.getElementById('metric-total').textContent = totalCount;
    document.getElementById('metric-os').textContent = osCount;
    document.getElementById('metric-saas').textContent = saasCount;
    document.getElementById('metric-mcp').textContent = mcpCount;
}

// Navegação entre abas
function initTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(btn => {
        btn.addEventListener('click', () => {
            tabs.forEach(b => {
                b.classList.remove('active', 'border-blue-500', 'text-blue-400', 'bg-blue-500/10');
                b.classList.add('text-slate-400', 'hover:text-slate-200');
            });
            btn.classList.add('active', 'border-blue-500', 'text-blue-400', 'bg-blue-500/10');
            btn.classList.remove('text-slate-400');

            activeTab = btn.dataset.tab;
            document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));
            document.getElementById(`tab-${activeTab}`).classList.remove('hidden');
        });
    });
}

// Configurar busca e filtros
function setupFiltersAndSearch() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.toLowerCase().trim();
            renderToolsList();
        });
    }

    const categorySelect = document.getElementById('category-filter');
    if (categorySelect) {
        categorySelect.addEventListener('change', (e) => {
            selectedCategory = e.target.value;
            renderToolsList();
        });
    }

    const filterPills = document.querySelectorAll('.filter-pill');
    filterPills.forEach(pill => {
        pill.addEventListener('click', () => {
            filterPills.forEach(p => {
                p.classList.remove('bg-blue-600', 'text-white');
                p.classList.add('bg-slate-800', 'text-slate-300');
            });
            pill.classList.add('bg-blue-600', 'text-white');
            pill.classList.remove('bg-slate-800', 'text-slate-300');

            activeFilter = pill.dataset.filter;
            renderToolsList();
        });
    });
}

// Renderizar grid de ferramentas no Catálogo Completo
function renderToolsList() {
    const container = document.getElementById('tools-grid');
    if (!container) return;

    let filtered = allTools.filter(t => {
        // Filtro por tipo rápido
        if (activeFilter === 'open-source' && t.tipo !== 'open-source') return false;
        if (activeFilter === 'saas' && (!t.tipo || (!t.tipo.includes('saas') && !t.tipo.includes('web') && !t.tipo.includes('banco') && !t.tipo.includes('plataforma')))) return false;
        if (activeFilter === 'mcp' && t.tipo !== 'mcp-servico-api') return false;

        // Filtro por categoria
        if (selectedCategory !== 'all' && t.categoria !== selectedCategory) return false;

        // Filtro por busca
        if (searchQuery) {
            const matchName = t.nome.toLowerCase().includes(searchQuery);
            const matchDesc = (t.descricao || '').toLowerCase().includes(searchQuery);
            const matchPot = (t.potencial_startuzeiro || '').toLowerCase().includes(searchQuery);
            const matchId = (t.id || '').toLowerCase().includes(searchQuery);
            if (!matchName && !matchDesc && !matchPot && !matchId) return false;
        }

        return true;
    });

    document.getElementById('filtered-count').textContent = `${filtered.length} ferramentas encontradas`;

    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="col-span-full text-center py-16 bg-slate-900/40 rounded-xl border border-dashed border-slate-800">
                <p class="text-slate-400 text-lg mb-2">Nenhuma ferramenta encontrada para os filtros selecionados.</p>
                <button onclick="resetFilters()" class="text-sm text-blue-400 hover:underline">Limpar filtros de busca</button>
            </div>
        `;
        return;
    }

    container.innerHTML = filtered.map(t => createToolCardHtml(t)).join('');
}

// Renderizar ferramentas Open-Source
function renderOpenSourceList() {
    const container = document.getElementById('opensource-grid');
    if (!container) return;

    const osTools = allTools.filter(t => t.tipo === 'open-source');
    container.innerHTML = osTools.map(t => createToolCardHtml(t, true)).join('');
}

// Renderizar diretório SaaS
function renderSaasList() {
    const container = document.getElementById('saas-grid');
    if (!container) return;

    const saasTools = allTools.filter(t => t.tipo && (t.tipo.includes('saas') || t.tipo.includes('web') || t.tipo.includes('banco') || t.tipo.includes('plataforma')));
    container.innerHTML = saasTools.map(t => createToolCardHtml(t)).join('');
}

function resetFilters() {
    searchQuery = '';
    selectedCategory = 'all';
    activeFilter = 'all';
    document.getElementById('search-input').value = '';
    document.getElementById('category-filter').value = 'all';
    renderToolsList();
}

// HTML do Card de Ferramenta
function createToolCardHtml(t, isOsOnly = false) {
    const catBadgeClass = getCategoryBadgeClass(t.categoria);
    const typeBadgeClass = getTypeBadgeClass(t.tipo);

    return `
        <div class="glass-panel p-5 rounded-xl flex flex-col justify-between transition-all duration-200 hover:-translate-y-1 hover:border-slate-600 cursor-pointer" onclick="openToolDrawer('${t.id}')">
            <div>
                <div class="flex items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-mono font-bold px-2 py-0.5 rounded bg-slate-800/80 text-blue-400 border border-slate-700">${t.id}</span>
                    <span class="text-xs px-2.5 py-0.5 rounded-full ${typeBadgeClass} font-medium">${t.tipo || 'ferramenta'}</span>
                </div>
                <h3 class="font-bold text-base text-white hover:text-blue-400 transition-colors mb-2 flex items-center gap-2">
                    ${escapeHtml(t.nome)}
                </h3>
                <p class="text-xs text-slate-400 leading-relaxed mb-4 line-clamp-3">
                    ${escapeHtml(t.descricao || '')}
                </p>
            </div>
            
            <div class="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                <span class="px-2 py-0.5 rounded ${catBadgeClass} font-medium">${escapeHtml(t.categoria || 'Geral')}</span>
                <span class="text-blue-400 font-semibold hover:underline flex items-center gap-1">
                    Ver usabilidade →
                </span>
            </div>
        </div>
    `;
}

// Mapeamento de Cores para Categorias
function getCategoryBadgeClass(cat) {
    if (!cat) return 'badge-design';
    if (cat.includes('osint')) return 'badge-osint';
    if (cat.includes('scraping')) return 'badge-scraping';
    if (cat.includes('video')) return 'badge-video';
    if (cat.includes('gtm') || cat.includes('prospeccao') || cat.includes('vendas')) return 'badge-gtm';
    if (cat.includes('agente')) return 'badge-agentes';
    if (cat.includes('engenharia')) return 'badge-engenharia';
    return 'badge-design';
}

function getTypeBadgeClass(tipo) {
    if (!tipo) return 'badge-saas';
    if (tipo === 'open-source') return 'badge-open-source';
    if (tipo.includes('mcp')) return 'badge-mcp';
    return 'badge-saas';
}

// Drawer / Slide-out Modal de Detalhes da Ferramenta
function openToolDrawer(toolId) {
    const tool = allTools.find(t => t.id === toolId);
    if (!tool) return;

    const drawer = document.getElementById('tool-drawer');
    const backdrop = document.getElementById('drawer-backdrop');
    const content = document.getElementById('drawer-content');

    const isOpenSource = tool.tipo === 'open-source';
    const isMcp = tool.tipo === 'mcp-servico-api';

    document.getElementById('drawer-title').textContent = tool.nome;
    document.getElementById('drawer-id').textContent = tool.id;
    document.getElementById('drawer-category').textContent = tool.categoria || 'Geral';
    document.getElementById('drawer-type').textContent = tool.tipo || 'ferramenta';
    document.getElementById('drawer-desc').textContent = tool.descricao || 'Sem descrição cadastrada.';
    document.getElementById('drawer-potencial').textContent = tool.potencial_startuzeiro || 'Sem potencial específico anotado.';
    
    const urlBtn = document.getElementById('drawer-link');
    urlBtn.href = tool.url || '#';
    urlBtn.textContent = tool.url ? `Acessar ${tool.nome} ↗` : 'Sem link';

    // Gerar comando rápido sugerido para cópia
    let quickCmd = '';
    if (isOpenSource) {
        if (tool.nome.toLowerCase().includes('mailaccess')) {
            quickCmd = 'uvx mailaccess doctor';
        } else if (tool.nome.toLowerCase().includes('scrapling')) {
            quickCmd = 'uv run --with scrapling python -c "import scrapling; print(\'Scrapling OK!\')"';
        } else if (tool.nome.toLowerCase().includes('changedetection')) {
            quickCmd = 'uv pip install changedetection.io && changedetection.io -p 5000';
        } else {
            quickCmd = `git clone ${tool.url}.git`;
        }
    } else if (isMcp) {
        if (tool.id === 'FER-062') {
            quickCmd = 'uv run scripts/utilitarios/clay_client.py search "select from companies where domain = \'google.com\'"';
        } else if (tool.id === 'FER-057') {
            quickCmd = 'npx ctx7@latest library react "hooks"';
        } else {
            quickCmd = `# Consultar skill .agents/skills/ correspondente a ${tool.nome}`;
        }
    } else {
        quickCmd = `# Abra no navegador: ${tool.url}`;
    }

    const cmdContainer = document.getElementById('drawer-cmd-container');
    const cmdText = document.getElementById('drawer-cmd-text');
    if (quickCmd) {
        cmdContainer.classList.remove('hidden');
        cmdText.textContent = quickCmd;
    } else {
        cmdContainer.classList.add('hidden');
    }

    // Exibir Drawer
    drawer.classList.remove('hidden');
    setTimeout(() => {
        backdrop.classList.remove('opacity-0');
        backdrop.classList.add('opacity-100');
        content.classList.remove('translate-x-full');
    }, 10);
}

function closeToolDrawer() {
    const backdrop = document.getElementById('drawer-backdrop');
    const content = document.getElementById('drawer-content');
    const drawer = document.getElementById('tool-drawer');

    backdrop.classList.remove('opacity-100');
    backdrop.classList.add('opacity-0');
    content.classList.add('translate-x-full');

    setTimeout(() => {
        drawer.classList.add('hidden');
    }, 300);
}

function copyDrawerCommand() {
    const text = document.getElementById('drawer-cmd-text').textContent;
    navigator.clipboard.writeText(text);
    const btn = document.getElementById('drawer-copy-btn');
    const orig = btn.textContent;
    btn.textContent = '✓ Copiado!';
    setTimeout(() => btn.textContent = orig, 2000);
}

// ========================================================
// Formulários e Execuções no Playground
// ========================================================
function setupPlaygroundForms() {
    // 1. Clay Form
    const clayBtn = document.getElementById('run-clay-btn');
    if (clayBtn) {
        clayBtn.addEventListener('click', async () => {
            const query = document.getElementById('clay-query-input').value.trim();
            const limit = document.getElementById('clay-limit-select').value;
            const consoleBox = document.getElementById('clay-console');

            if (!query) return alert('Por favor, digite uma query para o Clay.');

            consoleBox.textContent = `[*] Enviando query ao Clay via API Bridge...\nQuery: ${query}\nLimite: ${limit}\nAguarde...`;
            clayBtn.disabled = true;

            try {
                const res = await fetch('http://localhost:5050/api/run/clay', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query, limit })
                });
                const data = await res.json();
                if (data.error) {
                    consoleBox.textContent = `[!] Erro: ${data.error}`;
                } else {
                    consoleBox.textContent = (data.stdout || '') + (data.stderr ? `\n[STDERR]:\n${data.stderr}` : '');
                }
            } catch (err) {
                consoleBox.textContent = `[!] Falha de conexão: O servidor local não respondeu em http://localhost:5050.\nInicie o servidor rodando "uv run scripts/app_server.py" ou executando "abrir_painel.bat".\n\nErro detalhado: ${err.message}`;
            } finally {
                clayBtn.disabled = false;
            }
        });
    }

    // 2. YouTube Transcriber Form
    const ytBtn = document.getElementById('run-yt-btn');
    if (ytBtn) {
        ytBtn.addEventListener('click', async () => {
            const url = document.getElementById('yt-url-input').value.trim();
            const consoleBox = document.getElementById('yt-console');

            if (!url) return alert('Por favor, cole um link do YouTube.');

            consoleBox.textContent = `[*] Disparando yt_transcribe_and_catalog.py para:\n${url}\nExtraindo transcrição e metadados via TranscriptAPI...`;
            ytBtn.disabled = true;

            try {
                const res = await fetch('http://localhost:5050/api/run/youtube', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url })
                });
                const data = await res.json();
                if (data.error) {
                    consoleBox.textContent = `[!] Erro: ${data.error}`;
                } else {
                    consoleBox.textContent = (data.stdout || '') + (data.stderr ? `\n[STDERR]:\n${data.stderr}` : '');
                }
            } catch (err) {
                consoleBox.textContent = `[!] Falha de conexão com o servidor local (http://localhost:5050).\nInicie o servidor executando "abrir_painel.bat".`;
            } finally {
                ytBtn.disabled = false;
            }
        });
    }

    // 3. MailAccess Form
    const mailBtn = document.getElementById('run-mail-btn');
    if (mailBtn) {
        mailBtn.addEventListener('click', async () => {
            const action = document.getElementById('mail-action-select').value;
            const name = document.getElementById('mail-name-input').value.trim();
            const domain = document.getElementById('mail-domain-input').value.trim();
            const consoleBox = document.getElementById('mail-console');

            consoleBox.textContent = `[*] Executando MailAccess (${action})...\nAguarde...`;
            mailBtn.disabled = true;

            try {
                const res = await fetch('http://localhost:5050/api/run/mailaccess', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action, name, domain })
                });
                const data = await res.json();
                if (data.error) {
                    consoleBox.textContent = `[!] Erro: ${data.error}`;
                } else {
                    consoleBox.textContent = (data.stdout || '') + (data.stderr ? `\n[STDERR]:\n${data.stderr}` : '');
                }
            } catch (err) {
                consoleBox.textContent = `[!] Falha de conexão: Servidor local offline.\nInicie com "abrir_painel.bat".`;
            } finally {
                mailBtn.disabled = false;
            }
        });
    }

    // 4. Scrapling Form
    const scrapBtn = document.getElementById('run-scrapling-btn');
    if (scrapBtn) {
        scrapBtn.addEventListener('click', async () => {
            const url = document.getElementById('scrapling-url-input').value.trim();
            const consoleBox = document.getElementById('scrapling-console');

            if (!url) return alert('Por favor, informe a URL para raspar.');

            consoleBox.textContent = `[*] Executando Scrapling Fetcher com auto_match e bypass anti-bot...\nAlvo: ${url}\nAguarde...`;
            scrapBtn.disabled = true;

            try {
                const res = await fetch('http://localhost:5050/api/run/scrapling', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url })
                });
                const data = await res.json();
                if (data.error) {
                    consoleBox.textContent = `[!] Erro: ${data.error}`;
                } else {
                    consoleBox.textContent = (data.stdout || '') + (data.stderr ? `\n[STDERR]:\n${data.stderr}` : '');
                }
            } catch (err) {
                consoleBox.textContent = `[!] Falha de conexão: Servidor local offline.\nInicie com "abrir_painel.bat".`;
            } finally {
                scrapBtn.disabled = false;
            }
        });
    }

    // 5. Hunter Form
    const hunterBtn = document.getElementById('run-hunter-btn');
    if (hunterBtn) {
        hunterBtn.addEventListener('click', async () => {
            const domain = document.getElementById('hunter-domain-input').value.trim();
            const consoleBox = document.getElementById('hunter-console');

            if (!domain) return alert('Por favor, informe o domínio.');

            consoleBox.textContent = `[*] Consultando contagem de e-mails no Hunter.io para: ${domain}...`;
            hunterBtn.disabled = true;

            try {
                const res = await fetch('http://localhost:5050/api/run/hunter', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ domain })
                });
                const data = await res.json();
                if (data.error) {
                    consoleBox.textContent = `[!] Erro: ${data.error}`;
                } else {
                    consoleBox.textContent = JSON.stringify(data, null, 2);
                }
            } catch (err) {
                consoleBox.textContent = `[!] Falha de conexão: Servidor local offline.\nInicie com "abrir_painel.bat".`;
            } finally {
                hunterBtn.disabled = false;
            }
        });
    }

    // 6. cnpj.ai Form
    const cnpjBtn = document.getElementById('run-cnpj-btn');
    if (cnpjBtn) {
        cnpjBtn.addEventListener('click', () => {
            const cnpj = document.getElementById('cnpj-input').value.trim();
            const consoleBox = document.getElementById('cnpj-console');
            if (!cnpj) return alert('Por favor, digite um CNPJ.');

            const clean = cnpj.replace(/[^\d]/g, '');
            const basic = clean.substring(0, 8);
            const graphUrl = `https://grafo.cnpj.ai/?q=${basic}`;
            const portalUrl = `https://cnpj.ai/${clean}`;

            consoleBox.innerHTML = `
                <div class="space-y-3">
                    <p class="text-emerald-400 font-bold">✓ CNPJ Identificado: ${clean} (Básico: ${basic})</p>
                    <p class="text-slate-300">Acesse a rede societária e conexões da empresa:</p>
                    <div class="flex flex-wrap gap-2 pt-2">
                        <a href="${graphUrl}" target="_blank" class="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded text-xs font-semibold inline-flex items-center gap-1">
                            🌐 Abrir Grafo Societário Interativo ↗
                        </a>
                        <a href="${portalUrl}" target="_blank" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-xs font-semibold inline-flex items-center gap-1 border border-slate-700">
                            📄 Ver Ficha Completa no cnpj.ai ↗
                        </a>
                    </div>
                </div>
            `;
        });
    }
}

function copyConsoleOutput(elementId) {
    const el = document.getElementById(elementId);
    if (!el) return;
    navigator.clipboard.writeText(el.innerText || el.textContent);
    alert('Saída copiada para a área de transferência!');
}

function escapeHtml(string) {
    const entityMap = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
        '/': '&#x2F;'
    };
    return String(string).replace(/[&<>"'\/]/g, s => entityMap[s]);
}
