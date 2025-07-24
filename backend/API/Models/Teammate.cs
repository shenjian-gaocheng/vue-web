namespace API.Models;

public class Teammate
{
    public int Id { get; set; }
    public int SnhId { get; set; }
    public string Name { get; set; } = "";
    public bool IsTeamsii { get; set; }
    public bool IsTeamnew { get; set; }
    public bool IsActive { get; set; }
    public string? Url { get; set; }
    public string? Note { get; set; }
}
