export class Repo {
  id: number;
  name: string;
  full_name: string;
  url: string;
  git_url: string;
  clone_url: string;
  ssh_url: string;
  branches_url: string;
  default_branch: string;
  deployments_url: string;

  constructor(repo: any) {
    this.id = repo.id;
    this.name = repo.name;
    this.full_name = repo.full_name;
    this.url = repo.url;
    this.git_url = repo.git_url;
    this.clone_url = repo.clone_url;
    this.ssh_url = repo.ssh_url;
    this.branches_url = repo.branches_url;
    this.default_branch = repo.default_branch;
    this.deployments_url = repo.deployments_url;
  }
}

export class Branch {
  name: string;
  head_sha: string;

  constructor(branch: any) {
    this.name = branch.name;
    this.head_sha = branch.commit.sha;
  }
}

export class Compare {
  permalink_url: string;
  commits: string[];

  constructor(compare: any) {
      this.permalink_url = compare.permalink_url;
      this.commits = compare.commits;
  }
}