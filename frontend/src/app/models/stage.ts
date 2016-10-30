export class Stage {
    id: number;
    title: string;
    endpoint: string;   
    status: string;
    repo: string;
    branch: string;
    default_branch: string;
    created_at: number;

    run_on_create: boolean;
    compare_url: string;
    commits: string[];

    constructor(
        title: string,
        repo: string,
        branch: string,
        default_branch: string,
        run_on_create: boolean
    ) {
        this.title = title;
        this.repo = repo;
        this.branch = branch;
        this.default_branch = default_branch;
        this.run_on_create = run_on_create;
    }
}
