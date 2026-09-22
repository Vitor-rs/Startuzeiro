// Startuzeiro OS v2.0 - Core Frontend Controller
// CRM de Inteligência de Mercado, Fábrica de Pesquisa & Bancada Low-Code

const ACTIVE_TOOL_IDS = new Set([
    "FER-017",  // Scrapling
    "FER-023",  // Changedetection.io
    "FER-048",  // MailAccess
    "FER-057",  // Context7 MCP
    "FER-058",  // Exa MCP
    "FER-059",  // cnpj.ai MCP
    "FER-060",  // Hunter.io MCP
    "FER-061",  // Apollo.io MCP
    "FER-062",  // Clay MCP & CLI
    "FER-063",  // NetworkX
    "FER-064",  // GLiNER / GLiNER2
    "FER-067",  // MarkItDown
    "FER-069",  // PyMuPDF4LLM
    "FER-077",  // Instructor
    "FER-146",  // DuckDB
    "FER-203"   // Hugging Face Hub MCP
]);

let allTools = [];
let serverConnected = false;
let currentMainTab = 'orchestrator';
let currentStudio = 'diligence';
let currentCrmTab = 'dossiers';
let catalogFilter = 'all';
let selectedCategory = 'all';
let catalogSearchQuery = '';
let crmDossiers = [];
let crmOpportunities = [];
let crmLake = [];
let currentDossierRaw = '';
let d3Simulation = null;

// ========================================================
// INICIALIZAÇÃO
// ========================================================
document.addEventListener('DOMContentLoaded', async () => {
    initMainTabs();
    initStudioTabs();
    initCrmTabs();
    initCatalogFilters();
    initMissionControls();
    initStudioForms();
    
    await checkServerStatus();
    loadToolsCatalog();
    await refreshAllData();
});

// Atualização geral de dados
async function refreshAllData() {
    await Promise.all([
        fetchCrmDossiers(),
        fetchCrmOpportunities(),
        fetchCrmLake()
    ]);
    updateHeaderMetrics();
}

// Checagem de conectividade com o Backend
async function checkServerStatus() {
    const statusBadge = document.getElementById('server-status-badge');
    const statusText = document.getElementById('server-status-text');
    try {
        const res = await fetch('http://localhost:5050/api/status');
        if (res.ok) {
            const data = await res.json();
            serverConnected = true;
            statusBadge.className = 'inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 glow-emerald';
            statusText.textContent = `🟢 Servidor Ativo (${data.system} • Porta ${data.port})`;
            return;
        }
    } catch (e) {
        // Servidor offline
    }
    serverConnected = false;
    statusBadge.className = 'inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/15 text-amber-400 border border-amber-500/30';
    statusText.textContent = '🟡 Modo Estático (Inicie com abrir_painel.bat)';
}

// Carregar Catálogo de 203 Ferramentas
function loadToolsCatalog() {
    if (typeof TOOLS_DATA !== 'undefined' && Array.isArray(TOOLS_DATA)) {
        allTools = TOOLS_DATA.map(t => ({
            ...t,
            is_active: ACTIVE_TOOL_IDS.has(t.id)
        }));
    }
    populateCategoryDropdown();
    renderCatalog();
    updateHeaderMetrics();
}

function updateHeaderMetrics() {
    const elTotal = document.getElementById('metric-total');
    if (elTotal) elTotal.textContent = allTools.length || 203;

    const elActive = document.getElementById('metric-active');
    if (elActive) elActive.textContent = ACTIVE_TOOL_IDS.size;

    const elDossiers = document.getElementById('metric-dossiers');
    if (elDossiers) elDossiers.textContent = crmDossiers.length;

    const elOpps = document.getElementById('metric-opps');
    if (elOpps) elOpps.textContent = crmOpportunities.length;

    const elLake = document.getElementById('metric-lake');
    if (elLake) elLake.textContent = crmLake.length;

    const tabBadge = document.getElementById('tab-catalog-badge');
    if (tabBadge) tabBadge.textContent = allTools.length || 203;

    const crmDCount = document.getElementById('crm-dossiers-count');
    if (crmDCount) crmDCount.textContent = crmDossiers.length;

    const crmOCount = document.getElementById('crm-opps-count');
    if (crmOCount) crmOCount.textContent = crmOpportunities.length;

    const crmLCount = document.getElementById('crm-lake-count');
    if (crmLCount) crmLCount.textContent = crmLake.length;
}

// ========================================================
// CONTROLE DE NAVEGAÇÃO DE ABAS
// ========================================================
function initMainTabs() {
    const tabBtns = document.querySelectorAll('.main-tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            switchMainTab(btn.dataset.tab);
        });
    });
}

function switchMainTab(tabId) {
    currentMainTab = tabId;
    const tabBtns = document.querySelectorAll('.main-tab-btn');
    tabBtns.forEach(btn => {
        if (btn.dataset.tab === tabId) {
            btn.classList.add('active', 'border-blue-500', 'text-blue-400', 'bg-blue-500/10');
            btn.classList.remove('border-transparent', 'text-slate-400');
        } else {
            btn.classList.remove('active', 'border-blue-500', 'text-blue-400', 'bg-blue-500/10');
            btn.classList.add('border-transparent', 'text-slate-400');
        }
    });

    document.querySelectorAll('.main-tab-content').forEach(c => c.classList.add('hidden'));
    const targetContent = document.getElementById(`tab-${tabId}`);
    if (targetContent) targetContent.classList.remove('hidden');

    if (tabId === 'crm') {
        renderCrmDossiers();
        renderCrmOpportunities();
        renderCrmLake();
    }
}

function initStudioTabs() {
    const studioBtns = document.querySelectorAll('.studio-tab-btn');
    studioBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            switchStudio(btn.dataset.studio);
        });
    });
}

function switchStudio(studioId) {
    currentStudio = studioId;
    const studioBtns = document.querySelectorAll('.studio-tab-btn');
    studioBtns.forEach(btn => {
        if (btn.dataset.studio === studioId) {
            btn.className = 'studio-tab-btn active w-full text-left px-4 py-3 rounded-xl font-semibold text-xs flex items-center gap-2.5 transition bg-blue-600/20 text-blue-400 border border-blue-500/30';
        } else {
            btn.className = 'studio-tab-btn w-full text-left px-4 py-3 rounded-xl font-semibold text-xs flex items-center gap-2.5 transition bg-slate-900/60 text-slate-400 hover:text-slate-200 border border-slate-800/80';
        }
    });

    document.querySelectorAll('.studio-panel').forEach(p => p.classList.add('hidden'));
    const target = document.getElementById(`studio-${studioId}`);
    if (target) target.classList.remove('hidden');

    // Se abrir estúdio de due diligence, renderizar grafo se container vazio
    if (studioId === 'diligence' && !d3Simulation) {
        runNetworkXAction('demo');
    }
}

function initCrmTabs() {
    const crmBtns = document.querySelectorAll('.crm-subtab-btn');
    crmBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            currentCrmTab = btn.dataset.crm;
            crmBtns.forEach(b => {
                b.className = 'crm-subtab-btn px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700 transition';
            });
            btn.className = 'crm-subtab-btn active px-3 py-1.5 rounded-lg text-xs font-bold bg-purple-600 text-white transition';

            document.querySelectorAll('.crm-panel').forEach(p => p.classList.add('hidden'));
            const target = document.getElementById(`crm-view-${currentCrmTab}`);
            if (target) target.classList.remove('hidden');
        });
    });

    const searchInput = document.getElementById('crm-dossiers-search');
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            renderCrmDossiers(searchInput.value.toLowerCase().trim());
        });
    }
}

// ========================================================
// 1. FÁBRICA DE PESQUISA (ORQUESTRADOR DE MISSÕES 360°)
// ========================================================
function fillMissionExample(target, domain, cnpj) {
    document.getElementById('mission-target-input').value = target;
    document.getElementById('mission-domain-input').value = domain;
    document.getElementById('mission-cnpj-input').value = cnpj;
    document.getElementById('mission-notes-input').value = `Investigação de posicionamento de mercado, sócios-chave e infraestrutura tecnológica de ${target}.`;
}

function initMissionControls() {
    const runBtn = document.getElementById('run-mission-btn');
    if (!runBtn) return;

    runBtn.addEventListener('click', async () => {
        const targetName = document.getElementById('mission-target-input').value.trim();
        const domain = document.getElementById('mission-domain-input').value.trim();
        const cnpj = document.getElementById('mission-cnpj-input').value.trim();
        const notes = document.getElementById('mission-notes-input').value.trim();

        if (!targetName && !domain && !cnpj) {
            alert('Por favor, informe ao menos o Nome da empresa, Domínio corporativo ou CNPJ.');
            return;
        }

        const view = document.getElementById('mission-dossier-view');
        const statusSpan = document.getElementById('mission-dossier-status');
        const copyBtn = document.getElementById('btn-copy-dossier');
        const viewCrmBtn = document.getElementById('btn-view-crm');
        const timingSpan = document.getElementById('mission-timing');

        // Reset visual steps
        setPipelineStep('step-hunter', 'loading', 'Consultando base de e-mails do Hunter.io...');
        setPipelineStep('step-clay', 'pending', 'Aguardando...');
        setPipelineStep('step-cnpj', 'pending', 'Aguardando...');
        setPipelineStep('step-compile', 'pending', 'Aguardando...');

        runBtn.disabled = true;
        runBtn.innerHTML = '⏳ Orquestrando Missão 360°...';
        statusSpan.textContent = 'Executando pipeline multi-ferramenta...';
        view.innerHTML = `
            <div class="py-16 text-center text-slate-400 space-y-3">
                <div class="inline-block animate-spin text-2xl">⚙️</div>
                <p class="font-bold text-white">Investigando alvo: ${targetName || domain || cnpj}</p>
                <p class="text-xs text-slate-500">Coletando sinais no Hunter, Clay GTM, cnpj.ai e NetworkX...</p>
            </div>
        `;

        const startTime = Date.now();

        try {
            const res = await fetch('http://localhost:5050/api/orchestrator/mission', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    target_name: targetName,
                    domain: domain,
                    cnpj: cnpj,
                    notes: notes
                })
            });

            const data = await res.json();
            const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
            timingSpan.textContent = `Concluído em ${elapsed}s`;

            if (data.error) {
                statusSpan.textContent = 'Erro na execução da missão';
                view.innerHTML = `<div class="p-4 bg-red-950/40 border border-red-900/50 rounded-xl text-xs text-red-300">Erro: ${data.error}</div>`;
                return;
            }

            // Animar steps concluídos
            setPipelineStep('step-hunter', 'done', data.hunter ? `${data.hunter.total_emails} e-mails identificados` : 'Etapa concluída');
            setPipelineStep('step-clay', 'done', 'Pesquisa firmográfica executada');
            setPipelineStep('step-cnpj', 'done', data.cnpj_ai ? `Grafo mapeado (${data.cnpj_ai.cnpj})` : 'Alvo internacional');
            setPipelineStep('step-compile', 'done', `Dossiê gravado em ${data.dossier_path}`);

            currentDossierRaw = data.dossier_content || '';

            // Renderizar Markdown
            if (typeof marked !== 'undefined') {
                view.innerHTML = marked.parse(currentDossierRaw);
            } else {
                view.innerText = currentDossierRaw;
            }

            statusSpan.textContent = `🟢 Dossiê gravado no Lake (${data.dossier_path})`;
            copyBtn.classList.remove('hidden');
            viewCrmBtn.classList.remove('hidden');

            // Atualizar lista do CRM em background
            await fetchCrmDossiers();
            updateHeaderMetrics();

        } catch (err) {
            statusSpan.textContent = 'Falha de conexão com backend';
            view.innerHTML = `
                <div class="p-4 bg-amber-950/40 border border-amber-900/50 rounded-xl text-xs text-amber-300">
                    Não foi possível conectar ao servidor local na porta 5050.<br>
                    Certifique-se de executar <code>abrir_painel.bat</code> para disparar missões em tempo real.
                </div>
            `;
        } finally {
            runBtn.disabled = false;
            runBtn.innerHTML = '🚀 Iniciar Missão 360°';
        }
    });
}

function setPipelineStep(stepId, state, detail) {
    const el = document.getElementById(stepId);
    if (!el) return;
    const bullet = el.querySelector('.pipeline-bullet');
    const detailEl = el.querySelectorAll('div')[1];

    if (state === 'loading') {
        bullet.className = 'pipeline-bullet bg-blue-500 text-white animate-pulse';
        bullet.textContent = '⏳';
        el.className = 'pipeline-step text-blue-400 font-medium';
    } else if (state === 'done') {
        bullet.className = 'pipeline-bullet bg-emerald-500 text-white';
        bullet.textContent = '✓';
        el.className = 'pipeline-step text-emerald-400';
    } else {
        bullet.className = 'pipeline-bullet bg-slate-800 text-slate-500';
        el.className = 'pipeline-step text-slate-500';
    }

    if (detailEl && detail) detailEl.textContent = detail;
}

function copyMissionDossier() {
    if (!currentDossierRaw) return;
    navigator.clipboard.writeText(currentDossierRaw);
    alert('Dossiê em Markdown copiado com sucesso!');
}

// ========================================================
// 2. BANCADA LOW-CODE (WORKBENCH DE FERRAMENTAS)
// ========================================================
function initStudioForms() {
    // 1. Due Diligence / cnpj.ai
    const cnpjBtn = document.getElementById('run-studio-cnpj-btn');
    if (cnpjBtn) {
        cnpjBtn.addEventListener('click', async () => {
            const cnpjVal = document.getElementById('studio-cnpj-input').value.trim();
            const consoleBox = document.getElementById('studio-cnpj-console');
            const graphLink = document.getElementById('studio-cnpj-graph-link');

            if (!cnpjVal) return alert('Digite um CNPJ para pesquisar.');
            consoleBox.textContent = `[*] Consultando cnpj.ai para ${cnpjVal}...`;
            cnpjBtn.disabled = true;

            try {
                const res = await fetch('http://localhost:5050/api/workbench/cnpj', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cnpj: cnpjVal })
                });
                const data = await res.json();
                consoleBox.textContent = JSON.stringify(data, null, 2);
                if (data.grafo_url) {
                    graphLink.href = data.grafo_url;
                }
                // Renderizar nó no D3
                renderCustomGraphNode(data);
            } catch (e) {
                consoleBox.textContent = `[!] Servidor local offline ou erro de consulta.`;
            } finally {
                cnpjBtn.disabled = false;
            }
        });
    }

    // 3. Ingestor de Documentos
    const docBtn = document.getElementById('run-studio-doc-btn');
    if (docBtn) {
        docBtn.addEventListener('click', async () => {
            const pathVal = document.getElementById('studio-doc-path').value.trim();
            const previewBox = document.getElementById('studio-doc-preview');
            if (!pathVal) return alert('Informe o caminho do documento para converter.');

            previewBox.textContent = `[*] Ingerindo documento via MarkItDown / PyMuPDF4LLM: ${pathVal}...\nAguarde...`;
            docBtn.disabled = true;

            try {
                const res = await fetch('http://localhost:5050/api/workbench/document', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ file_path: pathVal })
                });
                const data = await res.json();
                if (data.error) {
                    previewBox.textContent = `[!] Erro: ${data.error}`;
                } else {
                    previewBox.textContent = (data.preview || data.stdout || 'Conversão concluída com sucesso.') + (data.stderr ? `\n[STDERR]:\n${data.stderr}` : '');
                }
            } catch (e) {
                previewBox.textContent = `[!] Falha de conexão com backend local.`;
            } finally {
                docBtn.disabled = false;
            }
        });
    }

    // 4. GLiNER NER
    const nerBtn = document.getElementById('run-studio-ner-btn');
    if (nerBtn) {
        nerBtn.addEventListener('click', async () => {
            const textVal = document.getElementById('studio-ner-text').value.trim();
            const labelsVal = document.getElementById('studio-ner-labels').value.split(',').map(s => s.trim()).filter(Boolean);
            const tagsBox = document.getElementById('studio-ner-tags');

            if (!textVal) return alert('Informe o texto para extrair entidades.');
            tagsBox.innerHTML = '<span class="text-xs text-blue-400 animate-pulse">Extraindo entidades com GLiNER zero-shot...</span>';
            nerBtn.disabled = true;

            try {
                const res = await fetch('http://localhost:5050/api/workbench/gliner', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: textVal, labels: labelsVal })
                });
                const data = await res.json();
                if (data.entities && data.entities.length > 0) {
                    tagsBox.innerHTML = data.entities.map(e => `
                        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs">
                            <span class="font-bold">${escapeHtml(e.text)}</span>
                            <span class="text-[10px] px-1 rounded bg-slate-800 text-slate-300 uppercase">${escapeHtml(e.label)}</span>
                            <span class="text-[10px] text-emerald-400 font-mono">${(e.score * 100).toFixed(0)}%</span>
                        </span>
                    `).join('');
                } else {
                    tagsBox.innerHTML = `<span class="text-xs text-slate-400">${data.raw || 'Nenhuma entidade detectada para os rótulos especificados.'}</span>`;
                }
            } catch (e) {
                tagsBox.innerHTML = `<span class="text-xs text-amber-400">Falha de conexão com servidor local.</span>`;
            } finally {
                nerBtn.disabled = false;
            }
        });
    }

    // 5. DuckDB Studio
    const duckBtn = document.getElementById('run-studio-duckdb-btn');
    if (duckBtn) {
        duckBtn.addEventListener('click', async () => {
            const query = document.getElementById('studio-duckdb-query').value.trim();
            const consoleBox = document.getElementById('studio-duckdb-console');
            if (!query) return alert('Digite a consulta SQL.');

            consoleBox.textContent = `[*] Executando SQL via DuckDB in-process...\n`;
            duckBtn.disabled = true;

            try {
                const res = await fetch('http://localhost:5050/api/workbench/duckdb', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                const data = await res.json();
                consoleBox.textContent = data.output || data.stderr || 'Consulta executada sem retorno textual.';
            } catch (e) {
                consoleBox.textContent = `[!] Falha de conexão com backend local.`;
            } finally {
                duckBtn.disabled = false;
            }
        });
    }

    // 6. YouTube Studio
    const ytBtn = document.getElementById('run-studio-yt-btn');
    if (ytBtn) {
        ytBtn.addEventListener('click', async () => {
            const urlVal = document.getElementById('studio-yt-url').value.trim();
            const consoleBox = document.getElementById('studio-yt-console');
            if (!urlVal) return alert('Informe a URL do vídeo do YouTube.');

            consoleBox.textContent = `[*] Transcrevendo e catalogando no Lake: ${urlVal}...\nAguarde...`;
            ytBtn.disabled = true;

            try {
                const res = await fetch('http://localhost:5050/api/workbench/youtube', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: urlVal })
                });
                const data = await res.json();
                consoleBox.textContent = (data.stdout || '') + (data.stderr ? `\n[STDERR]:\n${data.stderr}` : '');
                await fetchCrmLake();
                updateHeaderMetrics();
            } catch (e) {
                consoleBox.textContent = `[!] Falha de conexão com backend local.`;
            } finally {
                ytBtn.disabled = false;
            }
        });
    }

    // 7. Scrapling Studio
    const scrapBtn = document.getElementById('run-studio-scrapling-btn');
    if (scrapBtn) {
        scrapBtn.addEventListener('click', async () => {
            const urlVal = document.getElementById('studio-scrapling-url').value.trim();
            const consoleBox = document.getElementById('studio-scrapling-console');
            if (!urlVal) return alert('Informe a URL para raspar.');

            consoleBox.textContent = `[*] Executando Scrapling StealthyFetcher com bypass anti-bot...\nAlvo: ${urlVal}\nAguarde...`;
            scrapBtn.disabled = true;

            try {
                const res = await fetch('http://localhost:5050/api/workbench/scrapling', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: urlVal })
                });
                const data = await res.json();
                consoleBox.textContent = (data.stdout || '') + (data.stderr ? `\n[STDERR]:\n${data.stderr}` : '');
            } catch (e) {
                consoleBox.textContent = `[!] Falha de conexão com backend local.`;
            } finally {
                scrapBtn.disabled = false;
            }
        });
    }

    // 8. Hugging Face Explorer
    const hfBtn = document.getElementById('run-studio-hf-btn');
    if (hfBtn) {
        hfBtn.addEventListener('click', async () => {
            const queryVal = document.getElementById('studio-hf-query').value.trim();
            const typeVal = document.getElementById('studio-hf-type').value;
            const container = document.getElementById('studio-hf-results');

            if (!queryVal) return alert('Digite um termo para pesquisar no HF Hub.');
            container.innerHTML = '<div class="col-span-full text-center text-xs text-amber-400 py-6">Consultando Hugging Face Hub API...</div>';
            hfBtn.disabled = true;

            try {
                const res = await fetch('http://localhost:5050/api/workbench/huggingface', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: queryVal, type: typeVal })
                });
                const items = await res.json();
                if (Array.isArray(items) && items.length > 0) {
                    container.innerHTML = items.map(item => `
                        <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-1.5 hover:border-slate-700 transition">
                            <div class="flex items-center justify-between">
                                <span class="text-xs font-bold text-white truncate max-w-[200px]">${escapeHtml(item.id || item._id)}</span>
                                <span class="text-[10px] text-amber-400 font-mono">❤️ ${item.likes || 0}</span>
                            </div>
                            <div class="text-[11px] text-slate-400 flex items-center justify-between">
                                <span>Downloads: ${item.downloads || 0}</span>
                                <a href="https://huggingface.co/${item.id}" target="_blank" class="text-blue-400 hover:underline">Ver no Hub ↗</a>
                            </div>
                        </div>
                    `).join('');
                } else {
                    container.innerHTML = '<div class="col-span-full text-center text-xs text-slate-500 py-6">Nenhum repositório encontrado.</div>';
                }
            } catch (e) {
                container.innerHTML = '<div class="col-span-full text-center text-xs text-red-400 py-6">Falha ao consultar Hugging Face Hub.</div>';
            } finally {
                hfBtn.disabled = false;
            }
        });
    }
}

// Hunter Studio Caller
async function runHunterStudio(action) {
    const domain = document.getElementById('studio-hunter-domain').value.trim();
    const consoleBox = document.getElementById('studio-hunter-console');
    if (!domain) return alert('Informe o domínio.');

    consoleBox.textContent = `[*] Hunter.io (${action}) para: ${domain}...`;
    try {
        const res = await fetch('http://localhost:5050/api/workbench/hunter', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action, domain })
        });
        const data = await res.json();
        consoleBox.textContent = JSON.stringify(data, null, 2);
    } catch (e) {
        consoleBox.textContent = `[!] Servidor local offline ou erro de API.`;
    }
}

// Clay Studio Caller
async function runClayStudio() {
    const query = document.getElementById('studio-clay-query').value.trim();
    const consoleBox = document.getElementById('studio-clay-console');
    if (!query) return alert('Digite a query SQL-like.');

    consoleBox.textContent = `[*] Consultando banco da Clay com: ${query}...`;
    try {
        const res = await fetch('http://localhost:5050/api/workbench/clay', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, limit: 5 })
        });
        const data = await res.json();
        consoleBox.textContent = (data.stdout || '') + (data.stderr ? `\n[STDERR]:\n${data.stderr}` : '');
    } catch (e) {
        consoleBox.textContent = `[!] Servidor local offline ou erro na chamada.`;
    }
}

function setDuckDbSample(sql) {
    const queryEl = document.getElementById('studio-duckdb-query');
    if (queryEl) queryEl.value = sql;
}

// ========================================================
// VISUALIZADOR D3.JS DE GRAFOS SOCIETÁRIOS (NETWORKX)
// ========================================================
async function runNetworkXAction(action) {
    const consoleBox = document.getElementById('studio-cnpj-console');
    consoleBox.textContent = `[*] Executando NetworkX (${action})...\n`;

    try {
        const res = await fetch('http://localhost:5050/api/workbench/networkx', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action })
        });
        const data = await res.json();
        consoleBox.textContent = data.stdout || data.stderr || 'Comando executado.';

        // Renderizar grafo representativo no D3
        renderDemoGraphData();
    } catch (e) {
        consoleBox.textContent = `[!] Servidor offline. Renderizando simulação local no D3.`;
        renderDemoGraphData();
    }
}

function renderDemoGraphData() {
    const graphData = {
        nodes: [
            { id: "Holding Alpha", type: "company", r: 16, color: "#3b82f6" },
            { id: "Beta Ventures", type: "company", r: 14, color: "#3b82f6" },
            { id: "Gama Fin", type: "company", r: 14, color: "#3b82f6" },
            { id: "Carlos Silva", type: "person", r: 12, color: "#10b981" },
            { id: "Marina Costa", type: "person", r: 12, color: "#10b981" },
            { id: "Fundo Tech I", type: "company", r: 15, color: "#8b5cf6" }
        ],
        links: [
            { source: "Carlos Silva", target: "Holding Alpha", label: "Sócio-Adm (60%)" },
            { source: "Marina Costa", target: "Holding Alpha", label: "Sócia (40%)" },
            { source: "Holding Alpha", target: "Beta Ventures", label: "Controladora (100%)" },
            { source: "Holding Alpha", target: "Gama Fin", label: "Participação (51%)" },
            { source: "Fundo Tech I", target: "Beta Ventures", label: "Investidor Mútuo" }
        ]
    };
    renderD3Graph(graphData);
}

function renderCustomGraphNode(companyData) {
    const name = companyData.termo || "Alvo Pesquisado";
    const graphData = {
        nodes: [
            { id: name, type: "company", r: 16, color: "#3b82f6" },
            { id: "QSA / Sócios", type: "person", r: 12, color: "#10b981" },
            { id: "Administração", type: "person", r: 12, color: "#10b981" }
        ],
        links: [
            { source: "QSA / Sócios", target: name, label: "Quadro Societário" },
            { source: "Administração", target: name, label: "Representante Legal" }
        ]
    };
    renderD3Graph(graphData);
}

function renderD3Graph(data) {
    const container = document.getElementById('d3-graph-container');
    const svg = d3.select("#d3-graph-svg");
    const emptyState = document.getElementById('d3-empty-state');
    if (emptyState) emptyState.classList.add('hidden');

    svg.selectAll("*").remove();

    const width = container.clientWidth || 600;
    const height = container.clientHeight || 320;

    const g = svg.append("g");

    // Zoom behavior
    svg.call(d3.zoom()
        .scaleExtent([0.5, 3])
        .on("zoom", (event) => {
            g.attr("transform", event.transform);
        })
    );

    d3Simulation = d3.forceSimulation(data.nodes)
        .force("link", d3.forceLink(data.links).id(d => d.id).distance(90))
        .force("charge", d3.forceManyBody().strength(-240))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("collision", d3.forceCollide().radius(30));

    // Links
    const link = g.append("g")
        .selectAll("line")
        .data(data.links)
        .join("line")
        .attr("class", "graph-link")
        .attr("stroke", "#334155")
        .attr("stroke-width", 1.5);

    // Nodes
    const node = g.append("g")
        .selectAll("g")
        .data(data.nodes)
        .join("g")
        .attr("class", "graph-node")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended)
        )
        .on("click", (event, d) => {
            alert(`Nó Selecionado: ${d.id}\nTipo: ${d.type === 'company' ? 'Pessoa Jurídica' : 'Pessoa Física / Administrador'}`);
        });

    node.append("circle")
        .attr("r", d => d.r || 12)
        .attr("fill", d => d.color || "#3b82f6")
        .attr("stroke", "#1e293b");

    node.append("text")
        .attr("dy", -16)
        .attr("text-anchor", "middle")
        .text(d => d.id);

    d3Simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node.attr("transform", d => `translate(${d.x},${d.y})`);
    });

    function dragstarted(event, d) {
        if (!event.active) d3Simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) d3Simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
}

// ========================================================
// 3. CRM & ERP DE INTELIGÊNCIA DE MERCADO
// ========================================================
async function fetchCrmDossiers() {
    try {
        const res = await fetch('http://localhost:5050/api/crm/dossiers');
        if (res.ok) {
            crmDossiers = await res.json();
        }
    } catch (e) {
        crmDossiers = [];
    }
}

async function fetchCrmOpportunities() {
    try {
        const res = await fetch('http://localhost:5050/api/crm/opportunities');
        if (res.ok) {
            crmOpportunities = await res.json();
        }
    } catch (e) {
        crmOpportunities = [];
    }
}

async function fetchCrmLake() {
    try {
        const res = await fetch('http://localhost:5050/api/crm/lake');
        if (res.ok) {
            crmLake = await res.json();
        }
    } catch (e) {
        crmLake = [];
    }
}

function renderCrmDossiers(query = '') {
    const grid = document.getElementById('crm-dossiers-grid');
    if (!grid) return;

    let filtered = crmDossiers;
    if (query) {
        filtered = crmDossiers.filter(d => 
            d.title.toLowerCase().includes(query) || 
            (d.summary || '').toLowerCase().includes(query) ||
            d.filename.toLowerCase().includes(query)
        );
    }

    if (filtered.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full text-center py-12 bg-slate-900/40 rounded-2xl border border-dashed border-slate-800">
                <p class="text-slate-400 font-semibold mb-1">Nenhum dossiê de concorrente registrado.</p>
                <p class="text-xs text-slate-500 mb-3">Dispare uma investigação na "Fábrica de Pesquisa" para gerar o primeiro dossiê.</p>
                <button onclick="switchMainTab('orchestrator')" class="px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold">
                    Ir para Fábrica de Pesquisa 🚀
                </button>
            </div>
        `;
        return;
    }

    grid.innerHTML = filtered.map(d => `
        <div class="glass-panel p-5 rounded-2xl flex flex-col justify-between space-y-3 hover:border-slate-600 transition cursor-pointer" onclick="openDossierViewer('${escapeHtml(d.filename)}')">
            <div>
                <div class="flex items-center justify-between text-[11px] text-slate-400 mb-1">
                    <span class="font-mono text-blue-400">${escapeHtml(d.created_at)}</span>
                    <span class="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300">${d.size_kb} KB</span>
                </div>
                <h4 class="font-bold text-white text-base leading-snug mb-1">${escapeHtml(d.title)}</h4>
                <p class="text-xs text-slate-400 line-clamp-2">${escapeHtml(d.summary || 'Dossiê investigativo de mercado com mapeamento societário e de contatos.')}</p>
            </div>
            <div class="flex items-center justify-between pt-2 border-t border-slate-800/80 text-xs">
                <span class="text-slate-500 font-mono text-[10px] truncate max-w-[180px]">${escapeHtml(d.filename)}</span>
                <span class="text-blue-400 font-semibold hover:underline">Abrir Dossiê ↗</span>
            </div>
        </div>
    `).join('');
}

function renderCrmOpportunities() {
    const tbody = document.getElementById('crm-opportunities-tbody');
    if (!tbody) return;

    if (crmOpportunities.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-8 text-slate-500">
                    Nenhuma oportunidade catalogada em <code>oportunidades/</code>.
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = crmOpportunities.map(opp => {
        let statusBadge = 'bg-slate-800 text-slate-300';
        if (opp.status.includes('Validação')) statusBadge = 'bg-amber-500/20 text-amber-300 border border-amber-500/30';
        if (opp.status.includes('Ativo') || opp.status.includes('Aprovado')) statusBadge = 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';

        const ice = opp.ice_score || 0;
        let iceColor = 'text-slate-300';
        if (ice >= 20) iceColor = 'text-emerald-400 font-bold';
        else if (ice >= 10) iceColor = 'text-amber-400 font-bold';

        return `
            <tr class="hover:bg-slate-900/50 transition">
                <td class="py-3 px-4 font-mono text-blue-400 font-bold">${escapeHtml(opp.id)}</td>
                <td class="py-3 px-4 font-semibold text-white">${escapeHtml(opp.title)}</td>
                <td class="py-3 px-4 text-slate-400 uppercase text-[11px]">${escapeHtml(opp.category)}</td>
                <td class="py-3 px-4 text-center">
                    <span class="px-2 py-0.5 rounded text-[11px] ${statusBadge}">${escapeHtml(opp.status)}</span>
                </td>
                <td class="py-3 px-4 text-center font-mono ${iceColor}">${ice}</td>
                <td class="py-3 px-4 text-right">
                    <span class="text-slate-500 font-mono text-[11px]">${escapeHtml(opp.filename)}</span>
                </td>
            </tr>
        `;
    }).join('');
}

function renderCrmLake() {
    const tbody = document.getElementById('crm-lake-tbody');
    if (!tbody) return;

    if (crmLake.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center py-8 text-slate-500">
                    Nenhum vídeo no Lake catalogado em <code>yt_base/yt_lake/</code>.
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = crmLake.map(v => `
        <tr class="hover:bg-slate-900/50 transition">
            <td class="py-3 px-4 font-semibold text-white max-w-sm truncate">${escapeHtml(v.title)}</td>
            <td class="py-3 px-4 text-rose-300 font-medium">${escapeHtml(v.channel)}</td>
            <td class="py-3 px-4 text-slate-400 font-mono text-[11px]">${escapeHtml(v.date || '-')}</td>
            <td class="py-3 px-4 text-slate-400 font-mono text-[11px]">${v.size_kb} KB</td>
            <td class="py-3 px-4 text-right">
                <a href="${v.url || '#'}" target="_blank" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition">
                    Assistir ↗
                </a>
            </td>
        </tr>
    `).join('');
}

function openDossierViewer(filename) {
    const target = crmDossiers.find(d => d.filename === filename);
    if (!target) return;
    switchMainTab('orchestrator');
    const view = document.getElementById('mission-dossier-view');
    const statusSpan = document.getElementById('mission-dossier-status');
    statusSpan.textContent = `Visualizando: ${target.filename}`;
    view.innerHTML = `<div class="p-4 text-xs text-slate-300">Carregando arquivo <code>${target.path}</code>...</div>`;

    fetch(`../${target.path}`)
        .then(r => r.text())
        .then(content => {
            currentDossierRaw = content;
            if (typeof marked !== 'undefined') {
                view.innerHTML = marked.parse(content);
            } else {
                view.innerText = content;
            }
            document.getElementById('btn-copy-dossier').classList.remove('hidden');
        })
        .catch(err => {
            view.innerHTML = `<div class="p-4 text-xs text-red-400">Falha ao ler o arquivo markdown: ${err}</div>`;
        });
}

function openNewOpportunityModal() {
    const title = prompt("Título da Nova Oportunidade:");
    if (!title) return;
    const impact = prompt("Impacto (1 a 10):", "8") || "5";
    const confidence = prompt("Confiança (1 a 10):", "7") || "5";
    const ease = prompt("Facilidade (1 a 10):", "6") || "5";
    const ice = (parseFloat(impact) * parseFloat(confidence) * parseFloat(ease)).toFixed(0);

    alert(`Oportunidade "${title}" calculada com ICE Score = ${ice}.\nAdicione o arquivo Markdown correspondente em oportunidades/ para catalogação permanente no Lake.`);
}

// ========================================================
// 4. CATÁLOGO MASTER DE 203 FERRAMENTAS & AGENTE
// ========================================================
function initCatalogFilters() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            catalogSearchQuery = e.target.value.toLowerCase().trim();
            renderCatalog();
        });
    }

    const categorySelect = document.getElementById('category-filter');
    if (categorySelect) {
        categorySelect.addEventListener('change', (e) => {
            selectedCategory = e.target.value;
            renderCatalog();
        });
    }

    const pills = document.querySelectorAll('.filter-pill');
    pills.forEach(pill => {
        pill.addEventListener('click', () => {
            pills.forEach(p => {
                p.classList.remove('bg-blue-600', 'text-white');
                p.classList.add('bg-slate-800', 'text-slate-300');
            });
            pill.classList.add('bg-blue-600', 'text-white');
            pill.classList.remove('bg-slate-800', 'text-slate-300');

            catalogFilter = pill.dataset.filter;
            renderCatalog();
        });
    });
}

function populateCategoryDropdown() {
    const select = document.getElementById('category-filter');
    if (!select) return;

    const counts = {};
    allTools.forEach(t => {
        const cat = t.categoria || 'geral';
        counts[cat] = (counts[cat] || 0) + 1;
    });

    const sorted = Object.keys(counts).sort();
    select.innerHTML = `<option value="all">Todas as Categorias (${allTools.length})</option>` +
        sorted.map(c => {
            const label = c.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            return `<option value="${c}">${label} (${counts[c]})</option>`;
        }).join('');
}

function renderCatalog() {
    const container = document.getElementById('tools-grid');
    if (!container) return;

    let filtered = allTools.filter(t => {
        if (catalogFilter === 'active' && !t.is_active) return false;
        if (catalogFilter === 'open-source' && t.tipo !== 'open-source') return false;
        if (catalogFilter === 'saas' && (!t.tipo || (!t.tipo.includes('saas') && !t.tipo.includes('web') && !t.tipo.includes('banco') && !t.tipo.includes('plataforma')))) return false;
        if (catalogFilter === 'mcp' && t.tipo !== 'mcp-servico-api') return false;

        if (selectedCategory !== 'all' && t.categoria !== selectedCategory) return false;

        if (catalogSearchQuery) {
            const matchName = (t.nome || '').toLowerCase().includes(catalogSearchQuery);
            const matchDesc = (t.descricao || '').toLowerCase().includes(catalogSearchQuery);
            const matchId = (t.id || '').toLowerCase().includes(catalogSearchQuery);
            const matchPot = (t.potencial_startuzeiro || '').toLowerCase().includes(catalogSearchQuery);
            if (!matchName && !matchDesc && !matchId && !matchPot) return false;
        }

        return true;
    });

    document.getElementById('filtered-count').textContent = `${filtered.length} ferramentas exibidas`;

    if (filtered.length === 0) {
        container.innerHTML = `
            <div class="col-span-full text-center py-16 bg-slate-900/40 rounded-xl border border-dashed border-slate-800">
                <p class="text-slate-400 text-lg mb-2">Nenhuma ferramenta encontrada para os filtros selecionados.</p>
                <button onclick="resetCatalogFilters()" class="text-sm text-blue-400 hover:underline">Limpar filtros de busca</button>
            </div>
        `;
        return;
    }

    container.innerHTML = filtered.map(t => createToolCard(t)).join('');
}

function resetCatalogFilters() {
    catalogSearchQuery = '';
    selectedCategory = 'all';
    catalogFilter = 'all';
    document.getElementById('search-input').value = '';
    document.getElementById('category-filter').value = 'all';
    renderCatalog();
}

function createToolCard(t) {
    const isActive = t.is_active;
    const catClass = getCategoryBadgeClass(t.categoria);
    const typeClass = getTypeBadgeClass(t.tipo);

    const activeBadge = isActive 
        ? `<span class="badge-active-tool px-2 py-0.5 rounded text-[10px] font-bold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> ATIVA NA BANCADA</span>`
        : `<span class="badge-catalog-tool px-2 py-0.5 rounded text-[10px] font-medium">⚪ CATALOGADA</span>`;

    const actionButton = isActive
        ? `<button onclick="event.stopPropagation(); openToolInWorkbench('${t.id}')" class="px-2.5 py-1 rounded-lg bg-emerald-600/30 hover:bg-emerald-600/50 text-emerald-300 border border-emerald-500/40 text-xs font-semibold transition">
            🛠️ Abrir na Bancada
           </button>`
        : `<button onclick="event.stopPropagation(); openAgentRequestModal('${t.id}')" class="px-2.5 py-1 rounded-lg bg-blue-600/30 hover:bg-blue-600/50 text-blue-300 border border-blue-500/40 text-xs font-semibold transition flex items-center gap-1">
            🤖 Solicitar ao Agente
           </button>`;

    return `
        <div class="glass-panel p-5 rounded-2xl flex flex-col justify-between space-y-3 transition-all duration-200 hover:-translate-y-1 hover:border-slate-600 cursor-pointer ${isActive ? 'border-emerald-500/30' : ''}" onclick="openToolDrawer('${t.id}')">
            <div>
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-mono font-bold text-slate-400">${t.id}</span>
                    <div class="flex items-center gap-1.5">
                        <span class="${typeClass} px-2 py-0.5 rounded-full text-[10px] font-semibold">${formatType(t.tipo)}</span>
                        ${activeBadge}
                    </div>
                </div>

                <div class="mb-2">
                    <span class="${catClass} text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded inline-block mb-1">
                        ${(t.categoria || 'geral').replace(/-/g, ' ')}
                    </span>
                    <h3 class="text-base font-bold text-white leading-tight">${escapeHtml(t.nome)}</h3>
                </div>

                <p class="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-2">
                    ${escapeHtml(t.descricao || '')}
                </p>
            </div>

            <div class="pt-3 border-t border-slate-800/80 flex items-center justify-between gap-2">
                ${actionButton}
                <button onclick="event.stopPropagation(); openToolDrawer('${t.id}')" class="text-xs text-slate-400 hover:text-white transition">
                    Detalhes ↗
                </button>
            </div>
        </div>
    `;
}

// Abrir ferramenta diretamente no estúdio da bancada correspondente
function openToolInWorkbench(toolId) {
    switchMainTab('workbench');
    if (toolId === 'FER-059' || toolId === 'FER-063') switchStudio('diligence');
    else if (toolId === 'FER-060' || toolId === 'FER-061' || toolId === 'FER-062') switchStudio('gtm');
    else if (toolId === 'FER-067' || toolId === 'FER-069') switchStudio('ingestor');
    else if (toolId === 'FER-064') switchStudio('ner');
    else if (toolId === 'FER-146') switchStudio('duckdb');
    else if (toolId === 'FER-017' || toolId === 'FER-023') switchStudio('scrapling');
    else if (toolId === 'FER-203') switchStudio('huggingface');
    else switchStudio('diligence');
}

// Drawer de Detalhes
function openToolDrawer(toolId) {
    const t = allTools.find(x => x.id === toolId);
    if (!t) return;

    document.getElementById('drawer-id').textContent = t.id;
    document.getElementById('drawer-type').textContent = formatType(t.tipo);
    document.getElementById('drawer-type').className = `px-2.5 py-0.5 rounded-full text-xs font-medium ${getTypeBadgeClass(t.tipo)}`;
    
    const statusEl = document.getElementById('drawer-status');
    if (t.is_active) {
        statusEl.className = 'px-2 py-0.5 rounded text-[10px] font-bold badge-active-tool';
        statusEl.textContent = '🟢 ATIVA NA BANCADA';
    } else {
        statusEl.className = 'px-2 py-0.5 rounded text-[10px] font-medium badge-catalog-tool';
        statusEl.textContent = '⚪ CATALOGADA';
    }

    document.getElementById('drawer-category').textContent = (t.categoria || 'Geral').replace(/-/g, ' ');
    document.getElementById('drawer-title').textContent = t.nome;
    document.getElementById('drawer-desc').textContent = t.descricao || 'Sem descrição oficial informada.';
    document.getElementById('drawer-potencial').textContent = t.potencial_startuzeiro || 'Análise de usabilidade e testes no ecossistema Startuzeiro.';

    const cmdText = document.getElementById('drawer-cmd-text');
    if (t.is_active) {
        cmdText.textContent = `# Ferramenta ativa na bancada:\n# Utilize a aba 'Bancada Low-Code' para disparar sem terminal.`;
    } else {
        cmdText.textContent = `# Solicite ao Agente para instalar:\n# Clique no botão "Solicitar Instalação" abaixo para gerar o prompt.`;
    }

    document.getElementById('drawer-link').href = t.url || '#';

    const actionBtn = document.getElementById('drawer-action-btn');
    if (t.is_active) {
        actionBtn.textContent = '🛠️ Abrir na Bancada Low-Code';
        actionBtn.className = 'flex-1 py-2.5 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition shadow-lg shadow-emerald-600/20 truncate';
        actionBtn.onclick = () => { closeToolDrawer(); openToolInWorkbench(t.id); };
    } else {
        actionBtn.textContent = '🤖 Solicitar Instalação ao Agente';
        actionBtn.className = 'flex-1 py-2.5 px-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs transition shadow-lg shadow-blue-600/20 truncate';
        actionBtn.onclick = () => { closeToolDrawer(); openAgentRequestModal(t.id); };
    }

    const drawer = document.getElementById('tool-drawer');
    const backdrop = document.getElementById('drawer-backdrop');
    const content = document.getElementById('drawer-content');

    drawer.classList.remove('hidden');
    setTimeout(() => {
        backdrop.classList.remove('opacity-0');
        content.classList.remove('translate-x-full');
    }, 10);
}

function closeToolDrawer() {
    const drawer = document.getElementById('tool-drawer');
    const backdrop = document.getElementById('drawer-backdrop');
    const content = document.getElementById('drawer-content');

    backdrop.classList.add('opacity-0');
    content.classList.add('translate-x-full');
    setTimeout(() => {
        drawer.classList.add('hidden');
    }, 280);
}

function copyDrawerCommand() {
    const text = document.getElementById('drawer-cmd-text').innerText;
    navigator.clipboard.writeText(text);
    alert('Comando copiado!');
}

// Modal: Solicitar ao Agente
function openAgentRequestModal(toolId) {
    const t = allTools.find(x => x.id === toolId);
    if (!t) return;

    document.getElementById('agent-modal-id').textContent = t.id;
    document.getElementById('agent-modal-name').textContent = t.nome;

    const promptText = `Por favor, pesquise na internet, instale e configure a ferramenta catalogada ${t.id} (${t.nome}) no Startuzeiro:
- Categoria: ${t.categoria}
- Tipo: ${t.tipo}
- URL / Repo: ${t.url || 'Pesquisar no GitHub / PyPI'}
- Objetivo: ${t.potencial_startuzeiro || t.descricao}

Lembre-se da regra de ouro do Startuzeiro:
1. A infraestrutura deve ser menor que a pesquisa.
2. Evite instalar ferramentas pesadas ou duplicadas (sem redundância).
3. Se for open-source Python, integre via uv/pyproject.toml e crie o script wrapper em scripts/utilitarios/.
4. Ative a ferramenta no Startuzeiro OS adicionando seu ID à lista ACTIVE_TOOL_IDS em scripts/app_server.py e dashboard/app.js.`;

    document.getElementById('agent-modal-prompt').value = promptText;

    const modal = document.getElementById('agent-request-modal');
    modal.classList.remove('hidden');
}

function closeAgentRequestModal() {
    const modal = document.getElementById('agent-request-modal');
    modal.classList.add('hidden');
}

function copyAgentPrompt() {
    const promptText = document.getElementById('agent-modal-prompt').value;
    navigator.clipboard.writeText(promptText);
    const copyBtn = document.getElementById('agent-copy-btn');
    copyBtn.innerHTML = '✓ Prompt Copiado!';
    setTimeout(() => {
        copyBtn.innerHTML = '📋 Copiar Prompt';
    }, 2000);
}

// ========================================================
// UTILITÁRIOS DE FORMATAÇÃO E CORES
// ========================================================
function formatType(tipo) {
    if (!tipo) return 'Geral';
    if (tipo === 'open-source') return 'Open Source';
    if (tipo.includes('saas')) return 'SaaS';
    if (tipo === 'mcp-servico-api') return 'MCP / API';
    return tipo;
}

function getCategoryBadgeClass(cat) {
    if (!cat) return 'badge-osint';
    if (cat.includes('osint') || cat.includes('investigacao')) return 'badge-osint';
    if (cat.includes('scraping') || cat.includes('automacao')) return 'badge-scraping';
    if (cat.includes('video') || cat.includes('conteudo')) return 'badge-video';
    if (cat.includes('gtm') || cat.includes('sales')) return 'badge-gtm';
    if (cat.includes('agentes') || cat.includes('ia')) return 'badge-agentes';
    if (cat.includes('design')) return 'badge-design';
    return 'badge-engenharia';
}

function getTypeBadgeClass(tipo) {
    if (!tipo) return 'badge-saas';
    if (tipo === 'open-source') return 'badge-open-source';
    if (tipo === 'mcp-servico-api') return 'badge-mcp';
    return 'badge-saas';
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
