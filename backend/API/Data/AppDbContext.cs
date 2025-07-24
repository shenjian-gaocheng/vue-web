using Microsoft.EntityFrameworkCore;
using API.Models;

namespace API.Data;

public class AppDbContext : DbContext {
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) {}

    public DbSet<User> Users => Set<User>();
    public DbSet<Stage> Stages => Set<Stage>();
    public DbSet<Teammate> Teammates => Set<Teammate>();
}
