export interface Package {
    name: string;
    size_kb: number;
    description: string;
    manual: boolean;
}

export interface NodeModule {
    path: string;
    size_kb: number;
    last_modified: string; // ISO date string
}

export interface PnpmStore {
    path: string;
    size_kb: number;
}

export interface HomeDirItem {
    name: string;
    description: string;
}

export interface AiInsights {
    categorized_packages: string;
    explained_packages: string;
    explained_cryptic_packages: string;
    recommendations: string;
}

export interface AnalyzerData {
    manual_packages: Package[];
    node_modules: NodeModule[];
    pnpm_store: PnpmStore | null;
    home_dir_analysis: HomeDirItem[];
    ai_insights: AiInsights;
    generated_at: string;
}
