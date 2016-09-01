export class Stage {
    id: number;
    title: string;
    endpoint: string;   
    status: string;
    repo: string;
    default_branch: string;
    branch: string;
    created_at: number;

    compare_url: string;
    commits: string[];

    constructor(
        title: string,
        repo: string,
        default_branch: string,
        branch: string
    ) {
        this.title = title;
        this.repo = repo;
        this.default_branch = default_branch;
        this.branch = branch;
    }
}
