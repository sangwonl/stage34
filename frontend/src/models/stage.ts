export class Stage {
    id: number;
    title: string;
    endpoint: string;   
    status: string;
    repo_id: string;
    repo_name: string;
    branch_name: string;
    head_sha: string;
    commits: number;
    created_at: number;

    constructor(
        title: string,
        repo_id: string,
        repo_name: string,
        branch_name: string,
        head_sha: string
    ) {
        this.title = title;
        this.repo_id = repo_id;
        this.repo_name = repo_name;
        this.branch_name = branch_name;
        this.head_sha = head_sha;
    }
}
